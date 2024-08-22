#bin/bash

docker-compose -f cables/docker-compose.yaml down &&
docker-compose -f users/docker-compose.yaml down
