#!/bin/bash
export PROJECT=datascience
module purge
module load PrgEnv-cray
module load cray-mpich
module load craype-network-aries
module unload atp perftools-base/20.06.0 cray-libsci/20.06.1
module load conda
export CRAY_CPU_TARGET=x86-64
export CRAYPE_LINK_TYPE=dynamic
conda create --prefix /lus/theta-fs0/projects/$PROJECT/$USER/conda/envs/ss_env python=3.8 -y
conda activate /lus/theta-fs0/projects/$PROJECT/arigazzi/conda/envs/ss_env
pip install cmake
cd /lus/theta-fs0/projects/$PROJECT/$USER
mkdir smartsim-install
cd smartsim-install
git clone https://github.com/CrayLabs/SmartRedis.git smartredis
git clone https://github.com/CrayLabs/SmartSim.git smartsim
cd smartredis
export CC=$(which cc)
export CXX=$(which CC)
make lib && pip install .
cd ..
cd smartsim
conda install swig cmake git-lfs -y
pip install .[ml]
smart build --device cpu --onnx