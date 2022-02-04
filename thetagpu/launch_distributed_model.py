from smartsim import Experiment

"""
Create a simple model that runs a hello_world.c program

Make sure to have openmpi loaded,
this example runs in an interactive allocation.

i.e. qsub -n 3 -l walltime=01:00:00 -A <account> -q <queue> -I
"""

exp = Experiment("simple", launcher="auto")

# see https://www.craylabs.org/docs/api/smartsim_api.html#mpirunsettings
mpirun = exp.create_run_settings(
    "hello", run_command="mpirun"
)  # hello is name of executable
mpirun.set_tasks(40)
mpirun.set_task_map("node:PE=128")
mpirun.run_args["oversubscribe"] = None

# create a model with the settings we have defined
# this is like pythonic reference to a running job
hello_world = exp.create_model("hello_world", mpirun)

# create directory for output files of this model
exp.generate(hello_world, overwrite=True)

# start the model and block until completion
exp.start(hello_world, block=True, summary=True)

# get the status (should be Completed because we set block=True)
print(f"Model status: {exp.get_status(hello_world)}")
