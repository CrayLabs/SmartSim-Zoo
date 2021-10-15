
# SmartSim Example Zoo

This repository contains CrayLabs and user contibuted examples of using SmartSim
for various simulation and machine learning applications.

The CrayLabs team will attempt to keep examples updated with current releases
but all user contibuted examples should specify the release they were created
with.

### Contibuting Examples

We welcome any and all contibutions to this repository. The CrayLabs team will
do their best to review in a timely manner. We ask that, if you contribute examples,
please include a description and all references to code and relavent previous
implemenations or open source code that the work is based off of for the
benefit of anyone who would like to try out your example.

## Examples by Paper

The following examples are implemented based on existing research papers. Each
example lists the paper, previous works, and links to the implementation (possibly
stored within this repository or a seperate repository)


#### 1. [DeepDriveMD](https://github.com/CrayLabs/smartsim-openmm)

 - Contibuting User: CrayLabs
 - Tags: OpenMM, CVAE, online inference, unsupervised online learning, PyTorch, ensemble

This use case highlights many features of SmartSim and SmartRedis and
together they can be used to orchestrate complex workflows with coupled
applications without using the filesystem for exchanging information.

More specifically, this use case is based on the original DeepDriveMD work.
DeepDriveMD was furthered with an asynchronous streaming version. SmartSim
extends the streaming implementation through the use of the SmartSim
architecture. The main difference between the SmartSim implementation and
the previous implementations, is that neither ML models, nor Molecular
Dynamics (MD) intermediate results are stored on the file system. Additionally,
the inference portion of the workflow takes place inside the database instead of
a seperate task launched on the system.

 - [SmartSim Implementation](https://github.com/CrayLabs/smartsim-openmm)
 - [Previous Implementation](https://github.com/DeepDriveMD)
 - [Previous Implementation (streaming version)](https://github.com/DeepDriveMD/DeepDriveMD-streaming)
 - [DeepDriveMD Paper](https://arxiv.org/abs/1909.07817)
 - [Related Paper](https://github.com/DeepDriveMD/publications/blob/main/amaro-spike.rc1.pdf)

#### 2. [TensorFlowFoam](https://arxiv.org/abs/2012.00900)

- Contributing User: CrayLabs
- Tags: Online Inference, TensorFlow, OpenFOAM, supervised learning

This example shows how to use TensorFlow inside of OpenFOAM simulations using SmartSim.

More specifically, this SmartSim use case adapts the TensorFlowFoam work which utilized a deep neural network to predict steady-state turbulent viscosities of the Spalart-Allmaras (SA) model.  This use case highlights that a machine learning model can be evaluated using SmartSim from within a simulation with minimal external library code. For the OpenFOAM use case herein, only four SmartRedis client API calls are needed to initialize a client connection, send tensor data for evaluation, execute the TensorFlow model, and retrieve the model inference result.

In general, this example provides a useful driver script for those looking to run
OpenFOAM with SmartSim.

 - [SmartSim Implementation](https://github.com/CrayLabs/smartsim-openFOAM)
 - [Previous Implementation](https://github.com/argonne-lcf/TensorFlowFoam)
 - [Paper](https://arxiv.org/abs/2012.00900)


#### 3. [ML-EKE](https://github.com/CrayLabs/NCAR_ML_EKE)

 - Contributing User: CrayLabs
 - Tags: Online inference, MOM6, climate modeling, ensemble, parameterization replacement

This example was a collaboration between CrayLabs (HPE), NCAR, and the university of Victoria.
Using SmartSim, this example shows how to run an ensemble of simulations all using the
SmartSim architecture to replace a parameterization (MEKE) within each global ocean
simulation (MOM6).

Paper Abstract:

> We demonstrate the first climate-scale, numerical ocean simulations improved through distributed, online inference of Deep Neural Networks (DNN) using SmartSim. SmartSim is a library dedicated to enabling online analysis and Machine Learning (ML) for traditional HPC simulations. In this paper, we detail the SmartSim architecture and provide benchmarks including online inference with a shared ML model on heterogeneous HPC systems. We demonstrate the capability of SmartSim by using it to run a 12-member ensemble of global-scale, high-resolution ocean simulations, each spanning 19 compute nodes, all communicating with the same ML architecture at each simulation timestep. In total, 970 billion inferences are collectively served by running the ensemble for a total of 120 simulated years. Finally, we show our solution is stable over the full duration of the model integrations, and that the inclusion of machine learning has minimal impact on the simulation runtimes.


Since this is original research done by CrayLabs, there is no previous implementation.

 - [Implementation](https://github.com/CrayLabs/NCAR_ML_EKE)
 - [Paper](https://arxiv.org/abs/2104.09355)
 - [Seminar video](https://www.youtube.com/watch?v=2e-5j427AS0)

## Examples by Simulation Model

### [LAMMPS](https://www.lammps.org/)

SmartSim examples with LAMMPS which is a Molecular Dynamics simulation model.
#### 1. [Online Analysis of Atom Position](https://github.com/CrayLabs/smartsim-lammps)

 - Contibuting User: CrayLabs
 - Tags: Molecular Dynamics, online analysis, visualizations.

LAMMPS has ``dump`` styles which are custom I/O methods that can be implmentated
by users. CrayLabs implemented a ``SMARTSIM`` dump style which uses the SmartRedis
clients to stream data to an Orchestrator database created by SmartSim.

Once the data is in the database, any application with a SmartRedis client can consume
that data. For this example, we have a simple Python script that uses
[iPyVolume](https://github.com/maartenbreddels/ipyvolume) to plot the data every
100 iterations.

  - [Implementation](https://github.com/CrayLabs/smartsim-lammps)
  - [Forked LAMMPS model](https://github.com/CrayLabs/LAMMPS)

## Examples by System

High Performance Computing Systems are a bit like snowflakes, they are all different.
Since each one has their own quirks, some examples for specific and popular systems
can be of benefit to new users.

### National Center for Atmospheric Research (NCAR)

#### 1. Cheyenne

  - Contibuting User: CrayLabs
  - [implementation](https://github.com/CrayLabs/SmartSim-Zoo/tree/master/casper) (this repo)
  - WLM: PBSPro
  - System: SGI 8600
  - CPU: intel
  - GPU: None

#### 2. Casper

 - Contibuting user: @jedwards4b
 - [Implementation](https://github.com/CrayLabs/SmartSim-Zoo/tree/master/casper) (this repo)
 - WLM: PBSPro
 - GPU: Nvidia
 - CPU: Intel
 - SmartSim Version: 0.3.2
 - SmartRedis Version: 0.2.0

### Oak Ridge National Lab

#### 1. Summit

 - Contributing user: CrayLabs
 - [implementation](https://github.com/CrayLabs/SmartSim-Zoo/tree/master/summit) (this repo)
 - System:
 - OS: Red Hat Enterprise Linux (RHEL)
 - CPU: Power9
 - GPU: Nvidia V100
