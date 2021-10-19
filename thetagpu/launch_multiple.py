import os

from smartsim import Experiment
from smartsim.database import CobaltOrchestrator
from smartsim.settings import MpirunSettings


"""
Launch a distributed, in memory database cluster and a model that
sends data to the database.

This example runs in an interactive allocation with at least three
nodes and 2 processors per node. be sure to include mpirprocs in you
allocation.

i.e. qsub -n 3 -l walltime=00:20:00 -A <account> -q <queue> -I
"""

def collect_db_hosts(num_hosts):
    """A simple method to collect hostnames because we are using
       openmpi. (not needed for aprun(ALPS), Slurm, etc.)

       We append `.mcp` to each host name, as that is the
       name of the host attached to the high-bandwidth network.
    """

    hosts = []
    if "COBALT_NODEFILE" in os.environ:
        node_file = os.environ["COBALT_NODEFILE"]
        with open(node_file, "r") as f:
            for line in f.readlines():
                host = line.strip()
                hosts.append(host + ".mcp")
    else:
        raise Exception("could not parse interactive allocation nodes from COBALT_NODEFILE")

    if len(hosts) >= num_hosts:
        return hosts[:num_hosts]
    else:
        raise Exception(f"COBALT_NODEFILE had {len(hosts)} hosts, not {num_hosts}")


def launch_cluster_orc(experiment, hosts, port):
    """Just spin up a database cluster, check the status
       and tear it down"""

    print(f"Starting Orchestrator on hosts: {hosts}")
    # batch = False to launch on existing allocation
    db_cluster = CobaltOrchestrator(port=port,
                                db_nodes=3,
                                batch=False,
                                interface="enp226s0",
                                run_command="mpirun",
                                hosts=hosts)

    # generate directories for output files
    # pass in objects to make dirs for
    experiment.generate(db_cluster, overwrite=True)

    # start the database on interactive allocation
    experiment.start(db_cluster, block=True)

    # get the status of the database
    statuses = experiment.get_status(db_cluster)
    print(f"Status of all database nodes: {statuses}")

    return db_cluster

def create_producer(experiment):

    mpirun = MpirunSettings(exe="python",
                            exe_args="producer.py")
    mpirun.set_tasks(1)
    mpirun.set_task_map("node:PE=128")
    producer = experiment.create_model("producer", mpirun)

    # create directories for the output files and copy
    # scripts to execution location inside newly created dir
    # only necessary if its not an executable (python is executable here)
    producer.attach_generator_files(to_copy="./producer.py")
    experiment.generate(producer, overwrite=True)
    return producer

# create the experiment and specify Cobalt because ThetaGPU is a Cobalt system
exp = Experiment("launch_multiple", launcher="cobalt")

db_port = 6780
db_hosts = collect_db_hosts(3)
# start the database
db = launch_cluster_orc(exp, db_hosts, db_port)

model = create_producer(exp)
exp.start(model, block=True, summary=True)

# shutdown the database because we don't need it anymore
exp.stop(db)

print(exp.summary())


