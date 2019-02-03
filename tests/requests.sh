#!/usr/bin/env bash
# This shell script is a collection of curl commands to test the GRaaS openEO Core API

HOST="localhost"

# Get the capabilities
curl -X GET http://$HOST:5000/
# Collections
curl -X GET http://$HOST:5000/collections
# A single collection
curl -X GET http://$HOST:5000/collections/nc_spm_08.landsat.raster.lsat7_2000_80
# Processes
curl -X GET http://$HOST:5000/processes
# Processes process ids
curl -X GET http://$HOST:5000/processes/NDVI
curl -X GET http://$HOST:5000/processes/filter_bbox
curl -X GET http://$HOST:5000/processes/filter_daterange
