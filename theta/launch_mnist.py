from smartsim import Experiment
from smartsim.database import CobaltOrchestrator
from smartsim.settings import AprunSettings


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

def launch_orc(experiment, port):
    """Just spin up a single node database, check the status
    """

    # batch = False to launch on existing allocation
    db = CobaltOrchestrator(port=port,
                            db_nodes=1,
                            batch=False,
                            interface="ipogif0",
                            run_command="aprun")

    # generate directories for output files
    # pass in objects to make dirs for
    experiment.generate(db, overwrite=True)

    # start the database on interactive allocation
    experiment.start(db, block=True)

    # get the status of the database
    statuses = experiment.get_status(db)
    print(f"Status of all database nodes: {statuses}")

    print(f"Database started on {db.get_address()}")

    return db

def create_loader(experiment):

    aprun = AprunSettings(exe="python",
                          exe_args="mnist_loader.py")
    aprun.set_tasks(1)
    producer = experiment.create_model("loader", aprun)

    # create directories for the output files and copy
    # scripts to execution location inside newly created dir
    # only necessary if its not an executable (python is executable here)
    producer.attach_generator_files(to_copy=["./mnist_loader.py", "./mnist_script.py"],
                                    to_symlink=["./mnist"])
    experiment.generate(producer, overwrite=True)
    return producer

def create_trainer(experiment):

    aprun = AprunSettings(exe="python",
                          exe_args="mnist_trainer.py")
    aprun.set_tasks(1)
    producer = experiment.create_model("trainer", aprun)

    # create directories for the output files and copy
    # scripts to execution location inside newly created dir
    # only necessary if its not an executable (python is executable here)
    producer.attach_generator_files(to_copy="./mnist_trainer.py")
    experiment.generate(producer, overwrite=True)
    return producer

# create the experiment and specify Cobalt because Theta is a Cobalt system
exp = Experiment("launch_mnist", launcher="cobalt")

db_port = 6780
# start the database
db = launch_orc(exp, db_port)


trainer_model = create_trainer(exp)
exp.start(trainer_model, block=False, summary=False)

loader_model = create_loader(exp)
exp.start(loader_model, block=True, summary=False)

# shutdown the database because we don't need it anymore
exp.stop(db)

print(exp.summary())
