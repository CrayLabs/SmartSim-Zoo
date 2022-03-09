#!/usr/bin/bash
export PROJECT=datascience
module load conda
conda create --prefix /lus/theta-fs0/projects/$PROJECT/$USER/conda/envs/ss_env_gpu python=3.8 cmake git-lfs -y
conda activate /lus/theta-fs0/projects/$PROJECT/$USER/conda/envs/ss_env_gpu
cd /lus/theta-fs0/projects/$PROJECT/$USER
mkdir -p smartsim-install-gpu
cd smartsim-install-gpu
git clone https://github.com/CrayLabs/SmartRedis.git smartredis
git clone https://github.com/CrayLabs/SmartSim.git smartsim
cd smartredis
export CC=$(which gcc)
export CXX=$(which g++)
make lib && pip install . numpy==1.19.5 \
			  tensorflow==2.6.2 \
			  onnx==1.9.0 \
			  skl2onnx==1.10.3 \
			  onnxmltools==1.10.0 \
			  scikit-learn==1.0.2 \
			  torch==1.9.1+cu111 \
	          torchvision==0.10.1+cu111 \
	    	  torchaudio==0.9.1 \
	    	  -f https://download.pytorch.org/whl/torch_stable.html
cd ..
cd smartsim
pip install -e .[dev,ray]
export SMARTSIM_REDISAI=1.2.5
smart build --device gpu --onnx -v --torch_dir=/lus/theta-fs0/projects/$PROJECT/$USER/conda/envs/ss_env_gpu/lib/python3.8/site-packages/torch/share/cmake/Torch/
