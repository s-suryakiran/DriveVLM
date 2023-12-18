# DriveVLM

## Setup
Download and setup CARLA 0.9.10.1
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

Clone this repo and build the environment

```
git clone https://github.com/s-suryakiran/DriveVLM.git
cd DriveVLM
```

```
export PYTHONPATH=$PYTHONPATH:PATH_TO_DriveVLM
```

Create Dockerfile
```Dockerfile
FROM carlasim/carla:0.9.10.1
WORKDIR /home/carla/Import
COPY ./AdditionalMaps_0.9.10.1.tar.gz ./
WORKDIR /home/carla
RUN ./ImportAssets.sh
```

Run Dockerfile
- ```docker build -t carla:eval .```
- ```sudo docker run --privileged --gpus 0 -e SDL_VIDEODRIVER=offscreen -e SDL_HINT_CUDA_DEVICE=0 -p 2000-2002:2000-2002 -v /tmp/.X11-unix:/tmp/.X11-unix:rw -it carla:eval /bin/bash ./CarlaUE4.sh```

Install Python3.7:
```
 sudo apt update
 sudo apt install software-properties-common
 sudo add-apt-repository ppa:deadsnakes/ppa
 sudo apt install python3.7
 sudo apt-get install python3.7-distutils
```
Setup Python Virtual Environments:
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
