#bin/bash

docker-compose -f users/docker-compose.yaml up -d &&
docker-compose -f cables/docker-compose.yaml up -d