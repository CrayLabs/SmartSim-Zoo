from smartsim import Experiment
from smartsim.settings import CobaltBatchSettings, AprunSettings

"""
this example launches an ensemble of MPI hello_world
applications in a batch.

Before running this application:
 - load openmpi into your environment
 - compile hello.c
 - change the account number to your account

no allocation needs to be obtained before running
this example as the example will launch itself as a
batch workload
"""

account = "YOURACCOUNT"
queue = "YOURQUEUE"

exp = Experiment("batch_ensemble", launcher="cobalt")

# define resources available to the ensemble in batch

batch = CobaltBatchSettings(queue=queue, account=account, nodes=3, time='00:05:00')

# define how each member of the ensemble should
# be executed. in this case: aprun -n 10 ./hello
aprun = AprunSettings("hello")
aprun.set_tasks(10)


# create three replicas of the same model to run in a batch
hello_world = exp.create_ensemble("hello_world_ensemble",
                                  batch_settings=batch,
                                  run_settings=aprun,
                                  replicas=3)

# create directory for output files of this model
exp.generate(hello_world, overwrite=True)

# start the model and block until completion
exp.start(hello_world, block=True, summary=True)

# get the status (should be Completed because we set block=True)
print(f"Ensemble statuses: {exp.get_status(hello_world)}")

print(exp.summary())

