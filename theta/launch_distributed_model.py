from smartsim import Experiment

"""
Create a simple model that runs a hello_world.c program

Make sure to have openmpi loaded (module load openmpi)

this example runs in an interactive allocation.

i.e. qsub -n 3 -l walltime=01:00:00 -A <account> -q <queue> -I
"""

exp = Experiment("simple", launcher="auto")

# see https://www.craylabs.org/docs/api/smartsim_api.html#mpirunsettings
aprun = exp.create_run_settings("hello")  # hello is name of executable
aprun.set_tasks_per_node(20)
aprun.set_tasks(60)

# create a model with the settings we have defined
# this is like pythonic reference to a running job
hello_world = exp.create_model("hello_world", aprun)

# create directory for output files of this model
exp.generate(hello_world, overwrite=True)

# start the model and block until completion
exp.start(hello_world, block=True, summary=True)

# get the status (should be Completed because we set block=True)
print(f"Model status: {exp.get_status(hello_world)}")
