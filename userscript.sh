#!/bin/bash
echo "Install python"
sudo apt-get -y install python
echo "docker install"
sudo apt-get update -y && sudo apt-get install -y linux-image-extra-$(uname -r)
sudo apt-get install docker-engine -y
sudo service docker start
echo "pull docker image and runs service"
#sudo docker pull antongulenko/rtmp-nginx-server
sudo docker run antongulenko/rtmp-nginx-server &

sudo docker run -d --net="host" --pid="host" --privileged teambitflow/anomaly-injector-agent -host=wally166 -api-port 7999

#https://hub.docker.com/r/teambitflow/anomaly-injector-agent