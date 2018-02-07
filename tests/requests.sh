#!/usr/bin/env bash
# This shell script is a collection of curl commands to test the GRaaS openEO Core API

# get the swagger json description
curl -X GET http://localhost:5000/api/v0/swagger.json
# Capabilities
curl -X GET http://localhost:5000/capabilities
# Data
curl -X GET http://localhost:5000/data
# Data product id
curl -X GET http://localhost:5000/data/precipitation_1950_2013_yearly_mm@PERMANENT
# Processes
curl -X GET http://localhost:5000/processes
# Processes process ids
curl -X GET http://localhost:5000/processes/NDVI
curl -X GET http://localhost:5000/processes/filter_bbox
curl -X GET http://localhost:5000/processes/filter_daterange

