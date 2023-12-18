# DriveVLM

## Setup

### Prerequisites:
- cuda toolkit 12.1
- docker
- nvidia-container-toolkit for docker

### Download and setup CARLA 0.9.10.1:
```
mkdir carla
cd carla
wget https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/CARLA_0.9.10.1.tar.gz
wget https://carla-releases.s3.eu-west-3.amazonaws.com/Linux/AdditionalMaps_0.9.10.1.tar.gz
tar -xf CARLA_0.9.10.1.tar.gz
tar -xf AdditionalMaps_0.9.10.1.tar.gz
rm CARLA_0.9.10.1.tar.gz
rm AdditionalMaps_0.9.10.1.tar.gz
cd ..
```
Also update the ~/.bashrc file:
export CARLA_ROOT=PATH_TO_CARLA_0.9.10.1

### Clone this repo and build the environment:

```
git clone https://github.com/s-suryakiran/DriveVLM.git
cd DriveVLM
```

```
export PYTHONPATH=$PYTHONPATH:PATH_TO_DriveVLM
```

### Create Dockerfile:
```Dockerfile
FROM carlasim/carla:0.9.10.1
WORKDIR /home/carla/Import
COPY ./AdditionalMaps_0.9.10.1.tar.gz ./
WORKDIR /home/carla
RUN ./ImportAssets.sh
```

### Build Dockerfile:
- ```docker build -t carla:eval .```

### Install Python3.7:
```
 sudo apt update
 sudo apt install software-properties-common
 sudo add-apt-repository ppa:deadsnakes/ppa
 sudo apt install python3.7
 sudo apt-get install python3.7-distutils
```

### Setup Python Virtual Environments:
```
sudo apt-get install python3-pip
python3.10 -m pip install virtualenv
python3.10 -m virtualenv modelenv
source ./modelenv/bin/activate
pip install -r model_env_requirements.txt

python3.7 -m pip install virtualenv
python3.7 -m virtualenv tcpenv
source ./tcpenv/bin/activate
pip install -r tcp_env_requirements.txt
```

### Run the carla docker server:
- ```sudo docker run --privileged --gpus 0 -e SDL_VIDEODRIVER=offscreen -e SDL_HINT_CUDA_DEVICE=0 -p 2000-2002:2000-2002 -v /tmp/.X11-unix:/tmp/.X11-unix:rw -it carla:eval /bin/bash ./CarlaUE4.sh```

### To benchmark the reference TCP model:
- cd PATH_TO_DriveVLM
- make sure you started the carla docker server.
- Download their model - ```wget https://storage.googleapis.com/carla_dataset_bucket/Eval_Uploads/best_model.ckpt```
- Modify the ```TEAM_CONFIG``` in /leaderboard/scripts/run_evaluation.sh
- run the run_evaluation.sh - ```sh leaderboard/scripts/run_evaluation.sh```


## To benchmark our model:
- Update ```CARLA_ROOT``` with the root folder of CARLA_0.9.10.1 in sh leaderboard/scripts/run_evaluation_carla.sh
- Enable modelenv and start jupyter notebook server.
- Open Control_Prediction.ipynb and follow the steps there.
- After you run all the cells in the notebook, run
```sh leaderboard/scripts/run_evaluation_carla.sh```


# References:
- https://arxiv.org/abs/1711.03938
- https://arxiv.org/abs/2206.08129
- https://arxiv.org/abs/2308.12966