#!/bin/bash

# Use after Clean JetPack 3.2 install

#TODO: 
# Pre-build OpenCV
# Test without CUDA9 Installed
# Copy in S3 all external links
# Test with CUDA9/MXNet 1.x

# Prerequisits 
sudo apt update
sudo apt dist-upgrade -y
sudo apt install -y htop screen mplayer
sudo apt remove -y lightdm*
sudo apt remove -y network-manager* 

sudo echo '' | sudo tee -a /etc/network/interfaces
sudo echo 'auto eth0' | sudo tee -a /etc/network/interfaces
sudo echo 'iface eth0 inet dhcp' | sudo tee -a /etc/network/interfaces

sudo adduser --system ggc_user
sudo addgroup --system ggc_group

git clone https://github.com/aws-samples/aws-greengrass-samples.git
cd aws-greengrass-samples
cd greengrass-dependency-checker-GGCv1.5.0
sudo ./check_ggc_dependencies

# Cuda 8
sudo apt -y autoremove cuda-toolkit-9-0
sudo rm -f /etc/apt/sources.list.d/cuda-9-0-local.list
sudo rm -f /etc/apt/sources.list.d/nv-tensorrt-ga-cuda9.0-trt3.0.4-20180208.list
wget http://developer.download.nvidia.com/devzone/devcenter/mobile/jetpack_l4t/006/linux-x64/cuda-repo-l4t-8-0-local_8.0.34-1_arm64.deb
sudo dpkg -i cuda-repo-l4t-8-0-local_8.0.34-1_arm64.deb
sudo apt update
sudo apt -y install cuda-toolkit-8-0
sudo ln -s /usr/lib/aarch64-linux-gnu/libcudnn.so.7 /usr/lib/aarch64-linux-gnu/libcudnn.so.6

# MXNet 
mkdir mxnet
cd mxnet
wget https://s3.amazonaws.com/fx-greengrass-models/binaries/ggc-mxnet-v0.11.0-python-nvidia-tx2.tar.gz
tar -xvf ggc-mxnet-v0.11.0-python-nvidia-tx2.tar.gz
sudo sh mxnet_installer.sh

# Greengrass service

echo "[Unit]
Description=greengrass daemon
After=network.target

[Service]
ExecStart=/greengrass/ggc/core/greengrassd start
Type=simple
RestartSec=2
Restart=always
User=root
PIDFile=/var/run/greengrassd.pid

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/greengrass.service

sudo systemctl enable greengrass

# OpenCV
sudo apt remove -y libopencv 
git clone https://github.com/jetsonhacks/buildOpenCVTX2.git
cd buildOpenCVTX2/
./buildOpenCV.sh
cd $HOME/opencv/build
make
sudo make install


# TODO: install greengrass and certificates