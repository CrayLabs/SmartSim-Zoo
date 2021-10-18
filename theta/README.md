
# Theta Tutorials

Theta is the supercomputer at the Argonne National Lab. The
following tutorials are meant to aide users on Theta with getting used to the
different types of workflows that are possible with SmartSim.


## Prerequisites

On Theta, the launcher is Cobalt. SmartSim can be used to launch applications
with the `aprun` or `mpirun` commands.

The following module commands were utilized to run the examples

```bash
module purge
module load PrgEnv-cray
module load cray-mpich
module load craype-network-aries
module unload atp perftools-base/20.06.0 cray-libsci/20.06.1
module load conda
```

With this environment loaded, users will need to build and install both SmartSim and
SmartRedis through pip. Users are advised to build on
compute nodes, but the whole process can be run on any node.
Usually we recommend users installing or loading miniconda and
using the pip that comes with that installation. 

The following commands were utilized to build SmartSim on Theta,
after the needed Conda environment was loaded.

```bash
export CRAY_CPU_TARGET=x86-64
export CRAYPE_LINK_TYPE=dynamic
export CC=$(which cc)
export CXX=$(which CC)
conda install swig cmake git-lfs -y
pip install smartsim[ml]
smart --device cpu --onnx
```

Alternatively, if a bleeding-edge version of SmartSim or SmartRedis is
required, an installer script is available in this repository. It will
create a conda environment on the lustre filesystem (this can be modified): the
environment variable `PROJECT` has to be modified according to the user's
available project.

If you run into trouble with the installation, please consult the installation
documentation [here](https://www.craylabs.org/docs/installation.html).

## Examples

Three of the examples utilize interactive allocations, which is the preferred method of
launching SmartSim.

All the examples use `aprun` as a launch command. Examples for `mpirun` are available in the Theta GPU directory of this repository.

----------

### 1. launch_distributed_model.py

Launch a distributed model with `aprun` through SmartSim. This could represent
a simulation or other workload that contains the SmartRedis clients and commuicates
with the Orchestrator.

This example runs in an interactive allocation with at least three
nodes and 20 processors per node. 

```bash
# fill in account and queue parameters
qsub -n 3 -I --time=00:25:00 -A <account> -q <queue>
```

After obtaining the allocation, make sure to module load your conda or python environment
with SmartSim and SmartRedis installed.

Compile the simple hello world MPI program.

```bash
cc hello.c -o hello
```

Run the model through SmartSim in the interactive allocation

```bash
python launch_distributed_model.py
```

Instead of using an interactive allocation, SmartSim jobs can also be
launched through batch files. This is helpful when waiting a long time
for queued jobs.

The following gives an example of how you could launch the MPI
model above through a batch script instead of an interactive allocation.

```bash
#!/bin/bash
#COBALT -t 10
#COBALT -n 2
#COBALT -q <queue>
#COBALT -A <account>

# activate conda env if needed
python launch_distributed_model.py
```
---------

### 2. launch_database_cluster.py

This file shows how to launch a distributed ``Orchestrator`` (database cluster) and
utilize the SmartRedis Python client to communicate with it. This example is meant
to provide an example of how users can interact with the database in an interactive
fashion, possibly in a medium like a jupyter notebook.

This example runs in an interactive allocation with at least three
nodes and 2 processors per node. be sure to include mpiprocs in your
allocation.

```bash
# fill in account and queue parameters
qsub -l select=3:ncpus=1 -l walltime=00:20:00 -A <account> -q <queue> -I
```
After obtaining the allocation, make sure to module load your conda or python environment
with SmartSim and SmartRedis installed.

Run the workflow with

```bash
python launch_database_cluster.py
```
----------
### 3. launch_multiple.py

Launch an Orchestrator database in a cluster across three nodes and a data producer
that will put and get data from the Orchestrator using the SmartRedis Python client.

This example shows how a user can take the previous example a step further by
launching the application which communicates with the Orchestrator through SmartSim
as well.

It is important to note in this example that the database and producer are running
a converged workflow - that is, the database and application are placed on the same
nodes. Add a node(s) to the interactive allocation line if you wish for the data
producer to run on a seperate node.

```bash
# fill in account and queue parameters
qsub -n 3 -l walltime=00:20:00 -A <account> -q <queue> -I
```
After obtaining the allocation, make sure to module load your conda or python environment
with SmartSim and SmartRedis installed.

run the workflow with

```bash
python launch_multiple.py
```
-----------
### 4. launch_ensemble_batch.py

Launch a ensemble of hello world models in a batch created by SmartSim. This
file can be launched on a head node and will create a batch file for the all
the jobs to be launched.

The higher level batch capabilities of SmartSim allow users to create many
batch jobs of differing content without needing to write each one. As well,
SmartSim acts as a batch process manager in Python allowing interactivity
with the batch system to create pipelines, dependants, and conditions.

In this case, we create three replicas of the same model through the
``Experiment.create_ensemble()`` function. ``CobaltBatchSettings`` are created
to specify resources for the entire batch. ``AprunSettings`` are created
to specify how each member within the batch should be launched.

Before running the example, be sure to change the ``account`` number in the
file and any other batch settings for submission.

Then, compile the simple hello world MPI program.

```bash
cc hello.c -o hello
```

and run the workflow with

```bash
python launch_ensemble_batch.py
```



