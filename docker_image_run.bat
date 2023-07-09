cls
docker-compose down --remove-orphans
docker image rm --force crop-gen
docker-compose build --no-cache
docker-compose up