========================
The GRaaS openEO wrapper
========================

This software implements the openEO Core API interface for the GRASS GIS as a Service (GRaaS) solution.
GRaaS is an open source REST interface to process geodata with the GRASS GIS in a distributed environment.

Installation
============


1. Deploy the GRaaS installation using docker.

2. Make sure to deploy the GRASS GIS locations that are required for the GRaaS openEO wrapper test suite
   in the required GRaaS installation. Otherwise most if the tests will fail. The location data can be accessed here:

   .. code-block:: bash

      mkdir /$HOME/graas/grassdb
      cd /$HOME/graas/grassdb
      wget https://grass.osgeo.org/sampledata/north_carolina/nc_spm_08_grass7.tar.gz && \
           tar xzvf nc_spm_08_grass7.tar.gz && \
           rm -f nc_spm_08_grass7.tar.gz && \
           mv nc_spm_08_grass7 nc_spm_08
      wget https://storage.googleapis.com/datentransfer/ECAD.tar.gz && \
           tar xzvf ECAD.tar.gz && \
           rm -f ECAD.tar.gz
      wget https://storage.googleapis.com/datentransfer/LL.tar.gz && \
           tar xzvf LL.tar.gz && \
           rm -f LL.tar.gz



3. Create directory that should contain the code and the virtual environment and switch the environment.
It is preferred to run the openEO GRaaS wrapper in a virtual python environment:

   .. code-block:: bash

      mkdir openEO
      cd openEO
      virtualenv -p python3.5 venv
      source venv/bin/activate

4. Clone the official openEO reference implementation repository and install the required Python packages into the virtual environment:

   .. code-block:: bash

      git clone https://bitbucket.org/huhabla/openeo_core.git openeo_core
      cd openeo_core
      pip install -r requirements.txt
      python setup.py install

5. After installing the official openEO reference implementation the GRaaS openEO wrapper must be installed, since it is based on the reference implementation.

   .. code-block:: bash

      git clone https://bitbucket.org/huhabla/graas_openeo_core_wrapper.git graas_openeo_core_wrapper
      cd graas_openeo_core_wrapper
      pip install -r requirements.txt
      python setup.py install

6. Run the GRaaS openEO Core API test suite:

   .. code-block:: bash

      python setup.py test

7. Run the server:

   .. code-block:: bash

      python -m graas_openeo_core_wrapper.main

8. Get the swagger.json API description using curl:

   .. code-block:: bash

      curl -X GET http://localhost:5000/api/v0/swagger.json



================
openEO use cases
================

openEO use case 1
=================

The following commands show how the openEO use case 1, that was performed using the openEO GRaaS wrapper.
The command line tool *curl* was used ot perform the REST API calls.

First list all available data in the GRaaS database, the list was shortened, since aver 120 raster layer are
in the database:

   .. code-block:: bash

      curl http://127.0.0.1:5000/data

   .. code-block:: json

        [
          {
            "description": "Space time raster dataset",
            "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04",
            "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset"
          },
          {
            "description": "Space time raster dataset",
            "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08",
            "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset"
          },
          {
            "description": "Raster dataset",
            "product_id": "LL.sentinel2A_openeo_subset.raster.S2A_MSIL1C_20170412T110621_N0204_R137_T30SUJ_20170412T111708_B04",
            "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset"
          },
          {
            "description": "Raster dataset",
            "product_id": "LL.sentinel2A_openeo_subset.raster.S2B_MSIL1C_20170904T110619_N0205_R137_T30SUJ_20170904T111825_B08",
            "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset"
          },
          {
            "description": "Space time raster dataset",
            "product_id": "ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm",
            "source": "GRASS GIS location/mapset path: /ECAD/PERMANENT"
          },
          {
            "description": "Space time raster dataset",
            "product_id": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius",
            "source": "GRASS GIS location/mapset path: /ECAD/PERMANENT"
          },
          {
            "description": "Raster dataset",
            "product_id": "ECAD.PERMANENT.raster.precipitation_yearly_mm_0",
            "source": "GRASS GIS location/mapset path: /ECAD/PERMANENT"
          },
          {
            "description": "Raster dataset",
            "product_id": "ECAD.PERMANENT.raster.precipitation_yearly_mm_62",
            "source": "GRASS GIS location/mapset path: /ECAD/PERMANENT"
          },
          {
            "description": "Raster dataset",
            "product_id": "ECAD.PERMANENT.raster.temperature_mean_yearly_celsius_0",
            "source": "GRASS GIS location/mapset path: /ECAD/PERMANENT"
          },
          {
            "description": "Raster dataset",
            "product_id": "ECAD.PERMANENT.raster.temperature_mean_yearly_celsius_62",
            "source": "GRASS GIS location/mapset path: /ECAD/PERMANENT"
          },
        ]


Get information about band 04 of the sentinel2a  time series:

   .. code-block:: bash

      curl http://127.0.0.1:5000/data/LL.sentinel2A_openeo_subset.strds.S2A_B04

   .. code-block:: json

        {
          "aggregation_type": "None",
          "bands": {
            "band_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
          },
          "creation_time": "2018-02-13 23:43:42.579243",
          "description": "Space time raster dataset",
          "extent": {
            "bottom": 38.738166,
            "left": -5.333682,
            "right": -4.038089,
            "srs": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]\n",
            "top": 39.745573
          },
          "granularity": "1 second",
          "location": "LL",
          "map_time": "interval",
          "mapset": "sentinel2A_openeo_subset",
          "max_max": "22259.0",
          "max_min": "13773.0",
          "min_max": "0.0",
          "min_min": "0.0",
          "modification_time": "2018-02-13 23:43:43.126555",
          "number_of_maps": "7",
          "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04",
          "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset",
          "temporal_type": "2017-04-12 11:17:08",
          "time": {
            "from": "2017-04-12 11:17:08",
            "to": "2017-09-04 11:18:26"
          }
        }


Get information about band 08 of the sentinel2a  time series:

   .. code-block:: bash

      curl http://127.0.0.1:5000/data/LL.sentinel2A_openeo_subset.strds.S2A_B08

   .. code-block:: json

        {
          "aggregation_type": "None",
          "bands": {
            "band_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
          },
          "creation_time": "2018-02-13 23:43:43.581281",
          "description": "Space time raster dataset",
          "extent": {
            "bottom": 38.738166,
            "left": -5.333682,
            "right": -4.038089,
            "srs": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]\n",
            "top": 39.745573
          },
          "granularity": "1 second",
          "location": "LL",
          "map_time": "interval",
          "mapset": "sentinel2A_openeo_subset",
          "max_max": "23033.0",
          "max_min": "20256.0",
          "min_max": "0.0",
          "min_min": "0.0",
          "modification_time": "2018-02-13 23:43:44.111735",
          "number_of_maps": "7",
          "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08",
          "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset",
          "temporal_type": "2017-04-12 11:17:08",
          "time": {
            "from": "2017-04-12 11:17:08",
            "to": "2017-09-04 11:18:26"
          }
        }

List process information about all processes that are available for computation:

   .. code-block:: bash

      curl http://127.0.0.1:5000/processes

   .. code-block:: json

      [
        "udf_reduce_time",
        "min_time",
        "NDVI",
        "filter_daterange",
        "filter_bbox"
      ]


Get information about each available process:

   .. code-block:: bash

      curl http://127.0.0.1:5000/processes/udf_reduce_time

   .. code-block:: json

      {
        "args": {
          "collections": {
            "description": "array of input collections with one element"
          },
          "python_file_url": {
            "description": "The public URL to the python file that contains the udf"
          }
        },
        "description": "Apply a user defined function (UDF) to a time series of raster layers that produces a single raster layer as output.",
        "process_id": "udf_reduce_time"
      }

   .. code-block:: bash

      curl http://127.0.0.1:5000/processes/min_time

   .. code-block:: json

      {
        "args": {
          "collections": {
            "description": "array of input collections with one element"
          }
        },
        "description": "Finds the minimum value of time series for all bands of the input dataset.",
        "process_id": "min_time"
      }

   .. code-block:: bash

      curl http://127.0.0.1:5000/processes/NDVI

   .. code-block:: json

      {
        "args": {
          "collections": {
            "description": "array of input collections with one element"
          },
          "nir": {
            "description": "reference to the nir band"
          },
          "red": {
            "description": "reference to the red band"
          }
        },
        "description": "Compute the NDVI based on the red and nir bands of the input dataset.",
        "process_id": "NDVI"
      }

   .. code-block:: bash

      curl http://127.0.0.1:5000/processes/filter_daterange

   .. code-block:: json

      {
        "args": {
          "collections": {
            "description": "array of input collections with one element"
          },
          "from": {
            "description": "start date"
          },
          "to": {
            "description": "end date"
          }
        },
        "description": "Drops observations from a collection that have been captured before a start or after a given end date.",
        "process_id": "filter_daterange"
      }

   .. code-block:: bash

      curl http://127.0.0.1:5000/processes/filter_bbox

   .. code-block:: json

        {
          "args": {
            "bottom": {
              "description": "bottom boundary (latitude / northing)",
              "required": true
            },
            "collections": {
              "description": "array of input collections with one element"
            },
            "ewres": {
              "description": "East-west resolution in mapset units",
              "required": true
            },
            "left": {
              "description": "left boundary (longitude / easting)",
              "required": true
            },
            "nsres": {
              "description": "North-south resolution in mapset units",
              "required": true
            },
            "right": {
              "description": "right boundary (longitude / easting)",
              "required": true
            },
            "srs": {
              "description": "spatial reference system of boundaries as proj4 or EPSG:12345 like string"
            },
            "top": {
              "description": "top boundary (latitude / northing)",
              "required": true
            }
          },
          "description": "Drops observations from a collection that are located outside of a given bounding box.",
          "process_id": "filter_bbox"
        }

Create the process gaph as JSON code and send it via **curl** to the backend as a processing job:

   .. code-block:: bash

      JSON='{
          "process_graph": {
              "process_id": "min_time",
              "args": {
                  "collections": [{
                      "process_id": "NDVI",
                      "args": {
                          "collections": [{
                              "process_id": "filter_daterange",
                              "args": {
                                  "collections": [{
                                      "process_id": "filter_bbox",
                                      "args": {
                                          "collections": [{
                                              "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                          }],
                                          "left": -5.0,
                                          "right": -4.98,
                                          "top": 39.12,
                                          "bottom": 39.1,
                                          "ewres": 0.1,
                                          "nsres": 0.1,
                                          "srs": "EPSG:4326"
                                      }
                                  }],
                                  "from": "2017-04-12 11:17:08",
                                  "to": "2017-09-04 11:18:26"
                              }
                          },
                              {
                                  "process_id": "filter_daterange",
                                  "args": {
                                      "collections": [{
                                          "process_id": "filter_bbox",
                                          "args": {
                                              "collections": [{
                                                  "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                                              }],
                                              "left": -5.0,
                                              "right": -4.98,
                                              "top": 39.12,
                                              "bottom": 39.1,
                                              "ewres": 0.1,
                                              "nsres": 0.1,
                                              "srs": "EPSG:4326"
                                          }
                                      }],
                                      "from": "2017-04-12 11:17:08",
                                      "to": "2017-09-04 11:18:26"
                                  }
                              }],
                          "red": "S2A_B04",
                          "nir": "S2A_B08"
                      }
                  }]
              }
          }
      }'

   .. code-block:: bash

      curl -H "Content-Type: application/json" -X POST -d "${JSON}" http://127.0.0.1:5000/jobs

   .. code-block:: json

        {
          "job_id": "resource_id-ceaf3f1b-bbe9-41f4-b5f6-cb95815fb840",
          "job_info": {
            "accept_datetime": "2018-03-05 13:16:06.266574",
            "accept_timestamp": 1520255766.266574,
            "api_info": {
              "endpoint": "asyncpersistentresource",
              "method": "POST",
              "path": "/locations/LL/mapsets/openeo_mapset_0/processing_async",
              "request_url": "http://localhost:8080/locations/LL/mapsets/openeo_mapset_0/processing_async"
            },
            "datetime": "2018-03-05 13:16:06.267095",
            "http_code": 200,
            "message": "Resource accepted",
            "process_results": {},
            "resource_id": "resource_id-ceaf3f1b-bbe9-41f4-b5f6-cb95815fb840",
            "status": "accepted",
            "time_delta": 0.0005362033843994141,
            "timestamp": 1520255766.267094,
            "urls": {
              "resources": [],
              "status": "http://localhost:8080/status/user/resource_id-ceaf3f1b-bbe9-41f4-b5f6-cb95815fb840"
            },
            "user_id": "user"
          }
        }


We need to poll for the final result using the job id, since the request is asynchronous:

   .. code-block:: bash

      curl -X GET http://127.0.0.1:5000/jobs/resource_id-ceaf3f1b-bbe9-41f4-b5f6-cb95815fb840

   .. code-block:: json

        {
          "consumed_credits": 3.9191691875457764,
          "job_id": "resource_id-ceaf3f1b-bbe9-41f4-b5f6-cb95815fb840",
          "job_info": {
            "accept_datetime": "2018-03-05 13:16:06.266574",
            "accept_timestamp": 1520255766.266574,
            "api_info": {
              "endpoint": "asyncpersistentresource",
              "method": "POST",
              "path": "/locations/LL/mapsets/openeo_mapset_0/processing_async",
              "request_url": "http://localhost:8080/locations/LL/mapsets/openeo_mapset_0/processing_async"
            },
            "datetime": "2018-03-05 13:16:10.185691",
            "http_code": 200,
            "message": "Processing successfully finished",
            "process_log": [
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.12",
                  "s=39.1",
                  "e=-4.98",
                  "w=-5.0",
                  "ewres=0.1",
                  "nsres=0.1"
                ],
                "return_code": 0,
                "run_time": 0.05015707015991211,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "t.rast.extract",
                "parameter": [
                  "input=S2A_B04@sentinel2A_openeo_subset",
                  "where=start_time >= '2017-04-12 11:17:08' AND end_time <= '2017-09-04 11:18:26'",
                  "output=S2A_B04_filter_daterange",
                  "expression=1.0 * S2A_B04@sentinel2A_openeo_subset",
                  "basename=S2A_B04_extract",
                  "suffix=num"
                ],
                "return_code": 0,
                "run_time": 0.7367391586303711,
                "stderr": [
                  "Default TGIS driver / database set to:",
                  "driver: sqlite",
                  "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite.db",
                  "WARNING: Temporal database connection defined as:",
                  "/graas/workspace/temp_db/gisdbase_309978074dac48fea16dd328d1d0ebb1/LL/openeo_mapset_0/tgis/sqlite.db",
                  "But database file does not exist.",
                  "Creating temporal database: /graas/workspace/temp_db/gisdbase_309978074dac48fea16dd328d1d0ebb1/LL/openeo_mapset_0/tgis/sqlite.db",
                  "0..0..100",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.12",
                  "s=39.1",
                  "e=-4.98",
                  "w=-5.0",
                  "ewres=0.1",
                  "nsres=0.1"
                ],
                "return_code": 0,
                "run_time": 0.05015397071838379,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "t.rast.extract",
                "parameter": [
                  "input=S2A_B08@sentinel2A_openeo_subset",
                  "where=start_time >= '2017-04-12 11:17:08' AND end_time <= '2017-09-04 11:18:26'",
                  "output=S2A_B08_filter_daterange",
                  "expression=1.0 * S2A_B08@sentinel2A_openeo_subset",
                  "basename=S2A_B08_extract",
                  "suffix=num"
                ],
                "return_code": 0,
                "run_time": 0.8135900497436523,
                "stderr": [
                  "0..0..100",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "t.rast.mapcalc",
                "parameter": [
                  "expression=S2A_B08_filter_daterange_NDVI = float((S2A_B08_filter_daterange - S2A_B04_filter_daterange)/(S2A_B08_filter_daterange + S2A_B04_filter_daterange))",
                  "inputs=S2A_B08_filter_daterange,S2A_B04_filter_daterange",
                  "basename=ndvi",
                  "output=S2A_B08_filter_daterange_NDVI"
                ],
                "return_code": 0,
                "run_time": 0.7953689098358154,
                "stderr": [
                  "Starting temporal sampling...",
                  "Starting mapcalc computation...",
                  "14..28..42..57..71..85..100",
                  "Starting map registration in temporal database...",
                  "14..28..42..57..71..85..100",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "t.rast.colors",
                "parameter": [
                  "input=S2A_B08_filter_daterange_NDVI",
                  "color=ndvi"
                ],
                "return_code": 0,
                "run_time": 0.5513560771942139,
                "stderr": [
                  "Color table for raster map <ndvi_1@openeo_mapset_0> set to 'ndvi'",
                  "Color table for raster map <ndvi_2@openeo_mapset_0> set to 'ndvi'",
                  "Color table for raster map <ndvi_3@openeo_mapset_0> set to 'ndvi'",
                  "Color table for raster map <ndvi_4@openeo_mapset_0> set to 'ndvi'",
                  "Color table for raster map <ndvi_5@openeo_mapset_0> set to 'ndvi'",
                  "Color table for raster map <ndvi_6@openeo_mapset_0> set to 'ndvi'",
                  "Color table for raster map <ndvi_7@openeo_mapset_0> set to 'ndvi'",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "t.rast.series",
                "parameter": [
                  "input=S2A_B08_filter_daterange_NDVI",
                  "method=minimum",
                  "output=S2A_B08_filter_daterange_NDVI_min_time",
                  "-t"
                ],
                "return_code": 0,
                "run_time": 0.4821140766143799,
                "stderr": [
                  "0..100",
                  ""
                ],
                "stdout": ""
              }
            ],
            "process_results": {},
            "progress": {
              "num_of_steps": 7,
              "step": 7
            },
            "resource_id": "resource_id-ceaf3f1b-bbe9-41f4-b5f6-cb95815fb840",
            "status": "finished",
            "time_delta": 3.9191691875457764,
            "timestamp": 1520255770.185688,
            "urls": {
              "resources": [],
              "status": "http://localhost:8080/status/user/resource_id-ceaf3f1b-bbe9-41f4-b5f6-cb95815fb840"
            },
            "user_id": "user"
          },
          "last_update": "2018-03-05 13:16:10.185691",
          "process_graph": {
            "process_graph": {
              "args": {
                "collections": [
                  {
                    "args": {
                      "collections": [
                        {
                          "args": {
                            "collections": [
                              {
                                "args": {
                                  "bottom": 39.1,
                                  "collections": [
                                    {
                                      "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                    }
                                  ],
                                  "ewres": 0.1,
                                  "left": -5.0,
                                  "nsres": 0.1,
                                  "right": -4.98,
                                  "srs": "EPSG:4326",
                                  "top": 39.12
                                },
                                "process_id": "filter_bbox"
                              }
                            ],
                            "from": "2017-04-12 11:17:08",
                            "to": "2017-09-04 11:18:26"
                          },
                          "process_id": "filter_daterange"
                        },
                        {
                          "args": {
                            "collections": [
                              {
                                "args": {
                                  "bottom": 39.1,
                                  "collections": [
                                    {
                                      "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                                    }
                                  ],
                                  "ewres": 0.1,
                                  "left": -5.0,
                                  "nsres": 0.1,
                                  "right": -4.98,
                                  "srs": "EPSG:4326",
                                  "top": 39.12
                                },
                                "process_id": "filter_bbox"
                              }
                            ],
                            "from": "2017-04-12 11:17:08",
                            "to": "2017-09-04 11:18:26"
                          },
                          "process_id": "filter_daterange"
                        }
                      ],
                      "nir": "S2A_B08",
                      "red": "S2A_B04"
                    },
                    "process_id": "NDVI"
                  }
                ]
              },
              "process_id": "min_time"
            }
          },
          "status": "finished",
          "submitted": "2018-03-05 13:16:06.266574",
          "user_id": "user"
        }


Several raster time series datasets were produced in the process, that are now available:

   .. code-block:: bash

      curl http://127.0.0.1:5000/data

   .. code-block:: json

      [
          {
            "description": "Space time raster dataset",
            "product_id": "LL.openeo_mapset_0.strds.S2A_B04_filter_daterange",
            "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0"
          },
          {
            "description": "Space time raster dataset",
            "product_id": "LL.openeo_mapset_0.strds.S2A_B08_filter_daterange",
            "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0"
          },
          {
            "description": "Space time raster dataset",
            "product_id": "LL.openeo_mapset_0.strds.S2A_B08_filter_daterange_NDVI",
            "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0"
          },
          {
            "description": "Raster dataset",
            "product_id": "LL.openeo_mapset_0.raster.S2A_B08_filter_daterange_NDVI_min_time",
            "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0"
          }
      ]

We inspect the new NDVI time series:

   .. code-block:: bash

      curl http://127.0.0.1:5000/data/LL.openeo_mapset_0.strds.S2A_B08_filter_daterange_NDVI

   .. code-block:: json

        {
          "aggregation_type": "None",
          "bands": {
            "band_id": "LL.openeo_mapset_0.strds.S2A_B08_filter_daterange_NDVI"
          },
          "creation_time": "2018-03-05 13:16:08.887256",
          "description": "Space time raster dataset",
          "extent": {
            "bottom": 39.1,
            "left": -5.0,
            "right": -4.98,
            "srs": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]\n",
            "top": 39.12
          },
          "granularity": "1 second",
          "location": "LL",
          "map_time": "interval",
          "mapset": "openeo_mapset_0",
          "max_max": "0.457208",
          "max_min": "0.217788",
          "min_max": "0.457208",
          "min_min": "0.217788",
          "modification_time": "2018-03-05 13:16:08.909709",
          "number_of_maps": "7",
          "product_id": "LL.openeo_mapset_0.strds.S2A_B08_filter_daterange_NDVI",
          "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0",
          "temporal_type": "2017-04-12 11:17:08",
          "time": {
            "from": "2017-04-12 11:17:08",
            "to": "2017-09-04 11:18:26"
          }
        }

Information about the time reduced NDVI raster layer:

   .. code-block:: bash

      curl http://127.0.0.1:5000/data/LL.openeo_mapset_0.raster.S2A_B08_filter_daterange_NDVI_min_time

   .. code-block:: json

        {
          "description": "Raster dataset",
          "extent": {
            "bottom": 39.1,
            "left": -5.0,
            "right": -4.98,
            "srs": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]\n",
            "top": 39.12
          },
          "location": "LL",
          "mapset": "openeo_mapset_0",
          "product_id": "LL.openeo_mapset_0.raster.S2A_B08_filter_daterange_NDVI_min_time",
          "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0"
        }
