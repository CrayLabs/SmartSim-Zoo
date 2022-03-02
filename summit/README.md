
# Summit Tutorials

Summit is the supercomputer at Oak Ridge. The
following tutorials are meant to aide users on Summit with getting used to the
different types of workflows that are possible with SmartSim.


## Prerequisites

Summit users can use LSF (`jsrun`) as launcher.

The following modules were loaded to build the examples

```bash
  1) lsf-tools/2.0                6) nsight-systems/2021.3.1.54
  2) hsi/5.0.2.p5                 7) cuda/11.4.2
  3) darshan-runtime/3.3.0-lite   8) gcc/9.3.0
  4) DefApps                      9) spectrum-mpi/10.4.0.3-20210112
  5) nsight-compute/2021.2.1
```

Please refer to the documentation for how to build SmartSim and SmartRedis on
Summit [here](https://www.craylabs.org/docs/installation.html)

## Examples

Two of the examples utilize interactive allocations, which is the preferred method of
launching SmartSim.


----------

### 1. launch_distributed_model_lsf.py

Launch a distributed model with OpenMPI through SmartSim. This could represent
a simulation or other workload that contains the SmartRedis clients and communicates
with the Orchestrator.

This example runs in an interactive allocation with at least 40 processors, i.e. one node
is sufficient.

After obtaining the allocation, make sure to module load your conda or python environment
with SmartSim and SmartRedis installed, as well as the correct environment as shown above.

Compile the simple hello world MPI program with the correct environment loaded.

```bash
mpicc hello.c -o hello
```

Run the model through SmartSim in the interactive allocation. To use IBM Spectrum MPI
and `jsrun`

```bash
python launch_distributed_model_lsf.py
```

Instead of using an interactive allocation, SmartSim jobs can also be
launched through batch files. This is helpful when waiting a long time
for queued jobs.

The following gives an example of how you could launch the MPI
model above through a batch script instead of an interactive allocation.

```bash
#!/usr/bin/bash

#BSUB -W 00:10
#BSUB -P PROJECTNAME
#BSUB -J SmartSim
#BSUB -nnodes 1

# activate conda env if needed

# This is lsf
python launch_distributed_model_lsf.py
```
---------

### 2. launch_database_cluster.py

This file shows how to launch a distributed ``Orchestrator`` (database cluster) and
utilize the SmartRedis Python client to communicate with it. This example is meant
to provide an example of how users can interact with the database in an interactive
fashion, possibly in a medium like a jupyter notebook.

This example runs in an interactive allocation with at least three
nodes.

```bash
# fill in account and queue parameters
bsub -Is -W 01:00 -J SmartSim-int -nnodes 1 -P <project> -alloc_flags smt1 $SHELL
```
After obtaining the allocation, make sure to module load your conda or python environment
with SmartSim and SmartRedis installed.

Run the workflow with

```bash
python launch_database_cluster.py
```


