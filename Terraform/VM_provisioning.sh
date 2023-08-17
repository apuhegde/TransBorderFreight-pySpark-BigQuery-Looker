#!/bin/bash

#git clone https://github.com/apuhegde/TransBorderFreight-pySpark-BigQuery-Looker.git

sudo apt -y install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=$(dpkg --print-architecture)] https://download.docker.com/linux/ubuntu `lsb_release -cs` test"
sudo apt update
sudo apt -y install docker-ce
sudo apt -y install docker-ce-cli
sudo apt -y install containerd.io
sudo apt -y install docker-compose-plugin
sudo groupadd docker
sudo usermod -aG docker ${USER}
newgrp docker

#exit out of sub-shell
trap "exit 1" 10
PROC=$$
fatal(){
  echo "$@" >&2
  kill -10 $PROC
}

(fatal "Script exiting")

echo $(docker --version)
echo $(docker compose version)
