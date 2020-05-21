#!/bin/sh

docker build -t covid19-dev .
docker kill covid19-dev 2> /dev/null || true
docker run --rm --name covid19-dev -d -p 5002:5000 covid19-dev
