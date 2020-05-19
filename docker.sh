#!/bin/sh

docker build -t covid19 .
docker run --rm -d -p 5001:5000 covid19
