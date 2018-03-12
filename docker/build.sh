#!/bin/bash
# Build it
docker build -t graas_openeo_core_wrapper .
# Run it
docker run --name=graas_wrapper -p 5000:5000 graas_openeo_core_wrapper

curl http://openeo.mundialis.de:5000/data

docker ps
docker stop graas_openeo_core_wrapper && docker rm graas_openeo_core_wrapper

curl http://openeo.mundialis.de:5000/data
