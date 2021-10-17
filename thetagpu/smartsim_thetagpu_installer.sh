#!/bin/bash
export PROJECT=datascience
module load conda
conda create --prefix /lus/theta-fs0/projects/$PROJECT/$USER/conda/envs/ss_env_gpu python=3.8 -y
conda activate /lus/theta-fs0/projects/$PROJECT/$USER/conda/envs/ss_env_gpu
pip install cmake
cd /lus/theta-fs0/projects/$PROJECT/$USER
mkdir smartsim-install-gpu
cd smartsim-install-gpu
git clone https://github.com/CrayLabs/SmartRedis.git smartredis
git clone https://github.com/CrayLabs/SmartSim.git smartsim
cd smartredis
export CC=$(which gcc)
export CXX=$(which gxx)
make lib && pip install . numpy==1.19.5
cd ..
cd smartsim
conda install swig cmake git-lfs cudatoolkit cudnn -y
pip install . tensorflow==2.4.2 numpy==1.19.5 torch==1.7.1 onnx==1.7 
export CUDNN_LIBRARY_DIR=/lus/theta-fs0/projects/$PROJECT/$USER/conda/envs/ss_env_gpu/lib
export CUDNN_LIBRARY=/lus/theta-fs0/projects/$PROJECT/$USER/conda/envs/ss_env_gpu/lib
export CUDNN_INCLUDE_DIR=/lus/theta-fs0/projects/$PROJECT/$USER/conda/envs/ss_env_gpu/include
pip install .
smart --device gpu --onnx

