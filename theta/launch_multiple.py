from smartsim import Experiment
from smartsim.database import CobaltOrchestrator


def launch_cluster_orc(experiment, port):
    """Just spin up a database cluster, check the status
    and tear it down"""

    # batch = False to launch on existing allocation
    db_cluster = CobaltOrchestrator(
        port=port, db_nodes=3, batch=False, interface="ipogif0", run_command="aprun"
    )

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

    aprun = experiment.create_run_settings(exe="python", exe_args="producer.py")
    aprun.set_tasks(1)
    producer = experiment.create_model("producer", aprun)

    # create directories for the output files and copy
    # scripts to execution location inside newly created dir
    # only necessary if its not an executable (python is executable here)
    producer.attach_generator_files(to_copy="./producer.py")
    experiment.generate(producer, overwrite=True)
    return producer


# create the experiment and specify Cobalt because Theta is a Cobalt system
exp = Experiment("launch_multiple", launcher="auto")

db_port = 6780
# start the database
db = launch_cluster_orc(exp, db_port)

model = create_producer(exp)
exp.start(model, block=True, summary=True)

# shutdown the database because we don't need it anymore
exp.stop(db)

print(exp.summary())
