#!/bin/bash
# Build it
docker build -t openeo_grass_gis_driver_img .
# Run it
docker run --name=openeo_grass_gis_driver -p 5000:5000 openeo_grass_gis_driver_img

curl http://openeo.mundialis.de:5000/data

docker ps
docker stop openeo_grass_gis_driver && docker rm openeo_grass_gis_driver

curl http://openeo.mundialis.de:5000/data
