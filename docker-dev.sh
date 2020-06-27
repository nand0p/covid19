#!/bin/sh -ex

docker build --no-cache \
	     -t covid19-dev \
	     -f Dockerfile \
	     --build-arg "DATE=$(date +%s)" \
	     --build-arg "REVISION=$(git rev-parse HEAD)" \
	     .

docker kill covid19-dev 2> /dev/null || true
sleep 2
docker run --rm --name covid19-dev -d -p 5002:5000 covid19-dev
sleep 5
docker ps
echo "docker run --rm --name covid19-dev -ti -p 5002:5000 hex7-dev bash"
docker logs covid19-dev
