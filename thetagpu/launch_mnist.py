import os

from smartsim import Experiment
from smartsim.database import CobaltOrchestrator
from smartsim.settings import MpirunSettings


"""This driver starts an orchestrator, a loader, and a
   trainer process. 

   As on Theta the compute nodes cannot (easily) download
   MNIST, the user should download it (through PyTorch)
   into the same directory where this driver is launched.

   These are the stages in this example:
   - The processes are launched
   - The loader loads MNIST on the DB
   - The trainer gets MNIST from the DB
   - The trainer trains a ResNet18 model
   - The trainer puts the model on the DB
   - The loader loads the test dataset on the DB
   - The loader runs ResNet18 in inference mode to
     get the prediction on the test dataset
   - The laoder runs a script to compute the test
     accuracy on the DB, then retrieves it.

   Note that the inferred labels are not retrieved from the DB.
"""

def collect_hosts(num_hosts):
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


def launch_cluster_orc(experiment, host, port):
    """Just spin up a database cluster, check the status
       and tear it down"""

    print(f"Starting Orchestrator on host: {host}")
    # batch = False to launch on existing allocation
    db = CobaltOrchestrator(port=port,
                                db_nodes=1,
                                batch=False,
                                interface="enp226s0",
                                run_command="mpirun",
                                hosts=[host])

    # generate directories for output files
    # pass in objects to make dirs for
    experiment.generate(db, overwrite=True)

    # start the database on interactive allocation
    experiment.start(db, block=True)

    # get the status of the database
    statuses = experiment.get_status(db)
    print(f"Status of all database nodes: {statuses}")

    return db

def create_loader(experiment, host):

    mpirun = MpirunSettings(exe="python",
                            exe_args="mnist_loader.py")
    mpirun.set_tasks(1)
    mpirun.set_task_map("node:PE=128")
    mpirun.set_hostlist([host])
    loader = experiment.create_model("loader", mpirun)

    # create directories for the output files and copy
    # scripts to execution location inside newly created dir
    # only necessary if its not an executable (python is executable here)
    loader.attach_generator_files(to_copy=["./mnist_loader.py", "./mnist_script.py"],
                                  to_symlink=["./mnist"])
    experiment.generate(loader, overwrite=True)
    return loader


def create_trainer(experiment, host):

    mpirun = MpirunSettings(exe="python",
                            exe_args="mnist_trainer.py",
                            env_vars={"PYTHONUNBUFFERED": "1"})
    mpirun.set_tasks(1)
    mpirun.set_task_map("node:PE=128")
    mpirun.set_hostlist([host])
    trainer = experiment.create_model("trainer", mpirun)

    # create directories for the output files and copy
    # scripts to execution location inside newly created dir
    # only necessary if its not an executable (python is executable here)
    trainer.attach_generator_files(to_copy="./mnist_trainer.py")
    experiment.generate(trainer, overwrite=True)
    return trainer

# create the experiment and specify Cobalt because ThetaGPU is a Cobalt system
exp = Experiment("launch_mnist", launcher="cobalt")

db_port = 6780
hosts = collect_hosts(3)
# start the database
db = launch_cluster_orc(exp, hosts[0], db_port)

trainer_model = create_trainer(exp, hosts[1])
exp.start(trainer_model, block=False, summary=False)

loader_model = create_loader(exp, hosts[2])
exp.start(loader_model, block=True, summary=False)

# shutdown the database because we don't need it anymore
exp.stop(db)

print(exp.summary())


