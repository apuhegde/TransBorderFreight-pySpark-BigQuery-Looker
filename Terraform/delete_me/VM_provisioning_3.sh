#!/bin/bash

echo "Running the Docker installation script"

export PATH=$PATH:/usr/local/bin

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh > docker_install.log 2>&1

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose >> docker_install.log 2>&1
sudo chmod +x /usr/local/bin/docker-compose >> docker_install.log 2>&1