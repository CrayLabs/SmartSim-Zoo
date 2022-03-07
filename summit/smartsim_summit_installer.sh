# setup Python and build environment
export ENV_NAME=smartsim-0.4.0
git clone https://github.com/CrayLabs/SmartRedis.git smartredis
git clone https://github.com/CrayLabs/SmartSim.git smartsim
conda config --prepend channels https://ftp.osuosl.org/pub/open-ce/1.4.1/
conda create --name $ENV_NAME -y  python=3.9 \
                                  git-lfs \
                                  cmake \
                                  make \
                                  cudnn=8.1.1_11.2 \
                                  cudatoolkit=11.2.2 \
                                  tensorflow=2.6.2 \
                                  libtensorflow=2.6.2 \
                                  pytorch=1.9.0 \
                                  torchvision=0.10.0
conda activate $ENV_NAME
export CC=$(which gcc)
export CXX=$(which g++)
export LDFLAGS="$LDFLAGS -pthread"
export CUDNN_LIBRARY=/ccs/home/$USER/.conda/envs/$ENV_NAME/lib/
export CUDNN_INCLUDE_DIR=/ccs/home/$USER/.conda/envs/$ENV_NAME/include/
module load cuda/11.4.2
export LD_LIBRARY_PATH=$CUDNN_LIBRARY:$LD_LIBRARY_PATH:/ccs/home/$USER/.conda/envs/$ENV_NAME/lib/python3.9/site-packages/torch/lib
module load gcc/9.3.0
module unload xalt
# clone SmartRedis and build
pushd smartredis
make lib && pip install .
popd

# clone SmartSim and build
pushd smartsim
pip install .

# install PyTorch and TensorFlow backend for the Orchestrator database.
export Torch_DIR=/ccs/home/$USER/.conda/envs/$ENV_NAME/lib/python3.9/site-packages/torch/share/cmake/Torch/
export CFLAGS="$CFLAGS -I/ccs/home/$USER/.conda/envs/$ENV_NAME/lib/python3.9/site-packages/tensorflow/include"
export SMARTSIM_REDISAI=1.2.5
export Tensorflow_BUILD_DIR=/ccs/home/$USER/.conda/envs/$ENV_NAME/lib/python3.9/site-packages/tensorflow/
smart build --device=gpu --torch_dir $Torch_DIR --libtensorflow_dir $Tensorflow_BUILD_DIR -v

# Show LD_LIBRARY_PATH for future reference
echo "SmartSim installation is complete, LD_LIBRARY_PATH=$LD_LIBRARY_PATH"