#!/bin/bash

docker-compose rm -f
docker ps -a | grep scco_ | awk '{print $1}' | xargs docker rm
docker images -a | grep scco_ | awk '{print $3}' | xargs docker rmi -f
