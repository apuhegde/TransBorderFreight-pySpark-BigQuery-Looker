#!/bin/bash

sudo apt install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu `lsb_release -cs` test"
sudo apt update
sudo apt install docker-ce
sudo apt install docker-ce-cli
sudo apt install containerd.io
sudo apt install docker-compose-plugin
echo $(docker --version)
echo $(docker compose version)