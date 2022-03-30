  # setup Python and build environment
  export ENV_NAME=smartsim
  module load gcc/9.3.0
  module load cuda/11.0.3
  module load git-lfs
  module unload xalt
  git clone https://github.com/CrayLabs/SmartRedis.git 
  git clone https://github.com/CrayLabs/SmartSim.git 
  module load open-ce/1.4.0-py39-0
  conda create --clone open-ce-1.4.0-py39-0 --name smartsim
  conda activate $ENV_NAME
  conda install -c anaconda cmake -y
  export CC=$(which gcc)
  export CXX=$(which g++)
  export LDFLAGS="$LDFLAGS -pthread"
  export CUDNN_LIBRARY=/ccs/home/$USER/.conda/envs/$ENV_NAME/lib/
  export CUDNN_INCLUDE_DIR=/ccs/home/$USER/.conda/envs/$ENV_NAME/include/
  export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CUDNN_LIBRARY:/ccs/home/$USER/.conda/envs/$ENV_NAME/lib/python3.9/site-packages/torch/lib
  # clone SmartRedis and build
  pushd SmartRedis
  make lib && pip install .
  popd

  # clone SmartSim and build
  pushd SmartSim
  git clone https://github.com/CrayLabs/SmartSim.git
  pip install -e .[dev]
  popd

  # install PyTorch and TensorFlow backend for the Orchestrator database.
  export Torch_DIR=/ccs/home/$USER/.conda/envs/$ENV_NAME/lib/python3.9/site-packages/torch/share/cmake/Torch/
  export CFLAGS="$CFLAGS -I/ccs/home/$USER/.conda/envs/$ENV_NAME/lib/python3.9/site-packages/tensorflow/include"
  export SMARTSIM_REDISAI=1.2.5
  export Tensorflow_BUILD_DIR=/ccs/home/$USER/.conda/envs/$ENV_NAME/lib/python3.9/site-packages/tensorflow/
  smart build --device=gpu --torch_dir $Torch_DIR --libtensorflow_dir $Tensorflow_BUILD_DIR -v
