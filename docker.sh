#!/bin/sh

docker build -t covid19 .
docker kill covid19 2> /dev/null || true
docker run --rm --name covid19 -d -p 5000:5000 covid19
