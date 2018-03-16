===========================
The OpenEO GRASS GIS driver
===========================

The OpenEO GRASS GIS driver implements the openEO Core API interface for the GRASS GIS as a Service
(Actinia Core; available from https://github.com/mundialis/actinia_core) software solution for parallel,
large scale geodata processing.

It is a highly scalable REST interface to process geodata with the GRASS GIS in a distributed environment.
GRASS GIS is a free and open source software package providing geospatial processing engines in a single
integrated environment for raster, vector, and 3D-voxel processing as well as image processing capabilities.

It is deployed on **openeo.mundialis.de** and will be used for processing all openEO API calls that are send to
the the OpenEO GRASS GIS driver.

What is openEO?

    openEO - A Common, Open Source Interface between Earth Observation Data Infrastructures
    and Front-End Applications is an H2020 project funded under call EO-2-2017:
    EO Big Data Shift, under grant number 776242. The project runs from Oct 2017 to Sept 2020.

    http://openeo.org/

Purpose of this document

    This document demonstrates the application of the openEO Actinia Core wrapper to solve the three use cases
    that were defined by the development group for the first prototype:

    https://open-eo.github.io/openeo-api/poc/index.html#proof-of-concept


    Documentation reference page: https://open-eo.github.io/openeo-grassgis-driver/

Installation
============

An active internet connection is required. All requests to the openEO GRASS GIS driver will be send and processed on the **openeo.mundialis.de** server.

1. Deploy the openEO GRASS GIS driver locally:

    1. Create directory that should contain the code and the virtual environment and switch the environment.
       It is preferred to run the openEO Actinia Core wrapper in a virtual python environment:

       .. code-block:: bash

          mkdir openEO
          cd openEO
          virtualenv -p python3.5 venv
          source venv/bin/activate
       ..

    2. Clone the official python based openEO reference implementation repository and install
       the required Python packages into the virtual environment:

       .. code-block:: bash

          git clone https://bitbucket.org/huhabla/openeo_core.git openeo_core
          cd openeo_core
          pip install -r requirements.txt
          python setup.py install
          cd ..
       ..

    3. After installing the official python based openEO reference implementation, the openEO GRASS GIS driver
       must be installed, since it is based on the openEO reference implementation.

       .. code-block:: bash

          git clone https://github.com/Open-EO/openeo-grassgis-driver.git graas_openeo_core_wrapper
          cd graas_openeo_core_wrapper
          pip install -r requirements.txt
          python setup.py install
       ..

    4. Run the openEO GRASS GIS driver test suite (openEO wrapper test):

       .. code-block:: bash

          python setup.py test
       ..

       The test result should look like this:

          .. image:: OpenEO_GRaaS_Wrapper_Testsuite.png

    5. Run the server locally:

       .. code-block:: bash

          python -m graas_openeo_core_wrapper.main
       ..

2. Alternatively use the docker deployment located in the **docker** directory of this repository

    1. Make sure the GRaaS deployment is reachable by the openEO GRASS GIS driver container
    2. use the **build.sh** in the **docker** directory to build the image
    3. Deploy the openEO GRaaS docker container

        .. code-block:: bash

            cd graas_openeo_core_wrapper/docker
            docker build -t graas_openeo_core_wrapper .
            docker run --name=graas_wrapper -p 5000:5000 graas_openeo_core_wrapper
        ..

3. Get the swagger.json API description using curl:

   .. code-block:: bash

      curl -X GET http://openeo.mundialis.de:5000/api/v0/swagger.json

4. Explore the capabilities, data and processes that are available:

   .. code-block:: bash

      curl http://openeo.mundialis.de:5000/capabilities
      curl http://openeo.mundialis.de:5000/data
      curl http://openeo.mundialis.de:5000/processes


====================
The openEO use cases
====================

First list all available data in the GRaaS database, the list was shortened, since aver 120 raster layer are
in the database:

   .. code-block:: bash

      curl http://openeo.mundialis.de:5000/data

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

      curl http://openeo.mundialis.de:5000/data/LL.sentinel2A_openeo_subset.strds.S2A_B04

   .. code-block:: json

        {
          "aggregation_type": "None",
          "bands": {
            "band_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
          },
          "creation_time": "2018-02-13 23:43:42.579243",
          "description": "Space time raster dataset",
          "ewres_max": "0.0001",
          "ewres_min": "0.0001",
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
          "nsres_max": "0.0001",
          "nsres_min": "0.0001",
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

      curl http://openeo.mundialis.de:5000/data/LL.sentinel2A_openeo_subset.strds.S2A_B08

   .. code-block:: json

        {
          "aggregation_type": "None",
          "bands": {
            "band_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
          },
          "creation_time": "2018-02-13 23:43:43.581281",
          "description": "Space time raster dataset",
          "ewres_max": "0.0001",
          "ewres_min": "0.0001",
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
          "nsres_max": "0.0001",
          "nsres_min": "0.0001",
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

      curl http://openeo.mundialis.de:5000/processes

   .. code-block:: json

        [
          "raster_exporter",
          "filter_bbox",
          "udf_reduce_time",
          "filter_daterange",
          "NDVI",
          "min_time",
          "zonal_statistics"
        ]

Get information about each available process:

   .. code-block:: bash

      curl http://openeo.mundialis.de:5000/processes/raster_exporter

   .. code-block:: json

        {
          "args": {
            "collections": {
              "description": "array of input collections with one element that must be a raster layer"
            }
          },
          "description": "This process exports an arbitrary number of raster map layers using the region specified upstream.",
          "process_id": "raster_exporter"
        }

   .. code-block:: bash

      curl http://openeo.mundialis.de:5000/processes/udf_reduce_time

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

      curl http://openeo.mundialis.de:5000/processes/min_time

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

      curl http://openeo.mundialis.de:5000/processes/NDVI

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

      curl http://openeo.mundialis.de:5000/processes/filter_daterange

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

      curl http://openeo.mundialis.de:5000/processes/filter_bbox

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

   .. code-block:: bash

      curl http://openeo.mundialis.de:5000/processes/zonal_statistics

   .. code-block:: json

        {
          "args": {
            "imagery": {
              "description": "array of input collections with at least one element that must be of type time series"
            },
            "regions": {
              "description": "URL to a publicly accessible polygon file readable by OGR"
            }
          },
          "description": "Compute the zonal statistics of a time series using a vector polygon. The following parameters are computed: mean, min, max, mean_of_abs, stddev, variance, coeff_var, sum, null_cells, cells",
          "process_id": "zonal_statistics"
        }


openEO use case 1
=================

Use case one can be addressed in different ways using the openEO GRaaS wrapper. There are **POST** and **PUT**
calls for job creation that reflects the concept of persistent and ephemeral processing in GRaaS databases.

Persistent database approach
----------------------------

First, we use the **PUT** API call to solve use case 1 and store the result in the persistent database.

The following commands show the openEO use case 1 API calls and process graph creation.
The command line tool *curl* was used ot perform the REST API calls.

Create the process graph as JSON code and send it via **curl** to the backend as a processing job:

   .. code-block:: json

      {
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
                                          "collections": [{"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                          }],
                                          "bottom": 38.9,
                                          "left": -4.8,
                                          "right": -4.6,
                                          "top": 39.1,
                                          "ewres": 0.0001,
                                          "nsres": 0.0001,
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
                                              "bottom": 38.9,
                                              "left": -4.8,
                                              "right": -4.6,
                                              "top": 39.1,
                                              "ewres": 0.0001,
                                              "nsres": 0.0001,
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
      }

The JSON code must be stored in a shell variable and passed to the **curl** command:

   .. code-block:: bash

      JSON='{...}'

      curl -H "Content-Type: application/json" -X PUT -d "${JSON}" http://openeo.mundialis.de:5000/jobs

   .. code-block:: json

        {
          "job_id": "resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2",
          "job_info": {
            "accept_datetime": "2018-03-06 12:43:24.784656",
            "accept_timestamp": 1520340204.784654,
            "api_info": {
              "endpoint": "asyncpersistentresource",
              "method": "POST",
              "path": "/locations/LL/mapsets/openeo_mapset_0/processing_async",
              "request_url": "http://openeo.mundialis.de:8080/locations/LL/mapsets/openeo_mapset_0/processing_async"
            },
            "datetime": "2018-03-06 12:43:24.788535",
            "http_code": 200,
            "message": "Resource accepted",
            "process_results": {},
            "resource_id": "resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2",
            "status": "accepted",
            "time_delta": 0.003916025161743164,
            "timestamp": 1520340204.788534,
            "urls": {
              "resources": [],
              "status": "http://openeo.mundialis.de:8080/status/user/resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2"
            },
            "user_id": "user"
          }
        }

We need to poll for the final result using the job id, since the request is asynchronous:

   .. code-block:: bash

      curl -X GET http://openeo.mundialis.de:5000/jobs/resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2

   .. code-block:: json

        {
          "consumed_credits": 5.816864013671875,
          "job_id": "resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2",
          "job_info": {
            "accept_datetime": "2018-03-06 12:43:24.784656",
            "accept_timestamp": 1520340204.784654,
            "api_info": {
              "endpoint": "asyncpersistentresource",
              "method": "POST",
              "path": "/locations/LL/mapsets/openeo_mapset_0/processing_async",
              "request_url": "http://openeo.mundialis.de:8080/locations/LL/mapsets/openeo_mapset_0/processing_async"
            },
            "datetime": "2018-03-06 12:43:30.601449",
            "http_code": 200,
            "message": "Running executable t.rast.extract with parameters ['input=S2A_B04@sentinel2A_openeo_subset', \"where= ... subset', 'basename=S2A_B04_extract', 'suffix=num'] for 5.06658 seconds",
            "progress": {
              "num_of_steps": 7,
              "step": 2
            },
            "resource_id": "resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2",
            "status": "running",
            "time_delta": 5.816864013671875,
            "timestamp": 1520340210.601438,
            "urls": {
              "resources": [],
              "status": "http://openeo.mundialis.de:8080/status/user/resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2"
            },
            "user_id": "user"
          },
          "last_update": "2018-03-06 12:43:30.601449",
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
                                  "bottom": 38.9,
                                  "collections": [
                                    {
                                      "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                    }
                                  ],
                                  "ewres": 0.0001,
                                  "left": -4.8,
                                  "nsres": 0.0001,
                                  "right": -4.6,
                                  "srs": "EPSG:4326",
                                  "top": 39.1
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
                                  "bottom": 38.9,
                                  "collections": [
                                    {
                                      "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                                    }
                                  ],
                                  "ewres": 0.0001,
                                  "left": -4.8,
                                  "nsres": 0.0001,
                                  "right": -4.6,
                                  "srs": "EPSG:4326",
                                  "top": 39.1
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
          "resources": [],
          "status": "running",
          "submitted": "2018-03-06 12:43:24.784656",
          "user_id": "user"
        }


The final response will look like this:

   .. code-block:: bash

      curl -X GET http://openeo.mundialis.de:5000/jobs/resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2

   .. code-block:: json

        {
          "consumed_credits": 26.454089164733887,
          "job_id": "resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2",
          "job_info": {
            "accept_datetime": "2018-03-06 12:43:24.784656",
            "accept_timestamp": 1520340204.784654,
            "api_info": {
              "endpoint": "asyncpersistentresource",
              "method": "POST",
              "path": "/locations/LL/mapsets/openeo_mapset_0/processing_async",
              "request_url": "http://openeo.mundialis.de:8080/locations/LL/mapsets/openeo_mapset_0/processing_async"
            },
            "datetime": "2018-03-06 12:43:51.238708",
            "http_code": 200,
            "message": "Processing successfully finished",
            "process_log": [
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.1",
                  "s=38.9",
                  "e=-4.6",
                  "w=-4.8",
                  "ewres=0.0001",
                  "nsres=0.0001"
                ],
                "return_code": 0,
                "run_time": 0.05015993118286133,
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
                "run_time": 7.12386679649353,
                "stderr": [
                  "Default TGIS driver / database set to:",
                  "driver: sqlite",
                  "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite.db",
                  "WARNING: Temporal database connection defined as:",
                  "/graas/workspace/temp_db/gisdbase_0e7883deea584a8b8cb5e823390bfa7e/LL/openeo_mapset_0/tgis/sqlite.db",
                  "But database file does not exist.",
                  "Creating temporal database: /graas/workspace/temp_db/gisdbase_0e7883deea584a8b8cb5e823390bfa7e/LL/openeo_mapset_0/tgis/sqlite.db",
                  "0..0..100",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.1",
                  "s=38.9",
                  "e=-4.6",
                  "w=-4.8",
                  "ewres=0.0001",
                  "nsres=0.0001"
                ],
                "return_code": 0,
                "run_time": 0.05012702941894531,
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
                "run_time": 6.909211158752441,
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
                "run_time": 7.265884876251221,
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
                "run_time": 0.5597498416900635,
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
                "run_time": 2.155212879180908,
                "stderr": [
                  "0..3..6..9..12..15..18..21..24..27..30..33..36..39..42..45..48..51..54..57..60..63..66..69..72..75..78..81..84..87..90..93..96..99..100",
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
            "resource_id": "resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2",
            "status": "finished",
            "time_delta": 26.454089164733887,
            "timestamp": 1520340231.238706,
            "urls": {
              "resources": [],
              "status": "http://openeo.mundialis.de:8080/status/user/resource_id-af2ee1e7-71a4-48f0-953c-e3dacbf9c8c2"
            },
            "user_id": "user"
          },
          "last_update": "2018-03-06 12:43:51.238708",
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
                                  "bottom": 38.9,
                                  "collections": [
                                    {
                                      "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                    }
                                  ],
                                  "ewres": 0.0001,
                                  "left": -4.8,
                                  "nsres": 0.0001,
                                  "right": -4.6,
                                  "srs": "EPSG:4326",
                                  "top": 39.1
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
                                  "bottom": 38.9,
                                  "collections": [
                                    {
                                      "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                                    }
                                  ],
                                  "ewres": 0.0001,
                                  "left": -4.8,
                                  "nsres": 0.0001,
                                  "right": -4.6,
                                  "srs": "EPSG:4326",
                                  "top": 39.1
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
          "resources": [],
          "status": "finished",
          "submitted": "2018-03-06 12:43:24.784656",
          "user_id": "user"
        }

Several raster time series datasets were produced in the process, that are now available. We show only the new generated
rime series and the resulting NDVI raster layer:

   .. code-block:: bash

      curl http://openeo.mundialis.de:5000/data

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

      curl http://openeo.mundialis.de:5000/data/LL.openeo_mapset_0.strds.S2A_B08_filter_daterange_NDVI

   .. code-block:: json

        {
          "aggregation_type": "None",
          "bands": {
            "band_id": "LL.openeo_mapset_0.strds.S2A_B08_filter_daterange_NDVI"
          },
          "creation_time": "2018-03-06 12:43:46.814135",
          "description": "Space time raster dataset",
          "ewres_max": "0.0001",
          "ewres_min": "0.0001",
          "extent": {
            "bottom": 38.9,
            "left": -4.8,
            "right": -4.6,
            "srs": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]\n",
            "top": 39.1
          },
          "granularity": "1 second",
          "location": "LL",
          "map_time": "interval",
          "mapset": "openeo_mapset_0",
          "max_max": "0.869941",
          "max_min": "0.748342",
          "min_max": "-0.348271",
          "min_min": "-0.549595",
          "modification_time": "2018-03-06 12:43:46.832132",
          "nsres_max": "0.0001",
          "nsres_min": "0.0001",
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

      curl http://openeo.mundialis.de:5000/data/LL.openeo_mapset_0.raster.S2A_B08_filter_daterange_NDVI_min_time

   .. code-block:: json

        {
          "cells": "4000000",
          "cols": "2000",
          "comments": "\"r.series --overwrite file=\"/graas/workspace/temp_db/gisdbase_0e7883d\\eea584a8b8cb5e823390bfa7e/LL/openeo_mapset_0/.tmp/ba884fb4a052/44602\\.0\" output=\"S2A_B08_filter_daterange_NDVI_min_time\" method=\"minimum\"\\ quantile=\"",
          "datatype": "DCELL",
          "description": "Raster dataset",
          "ewres": "0.0001",
          "extent": {
            "bottom": 38.9,
            "left": -4.8,
            "right": -4.6,
            "srs": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]\n",
            "top": 39.1
          },
          "location": "LL",
          "mapset": "openeo_mapset_0",
          "nsres": "0.000100000000000001",
          "product_id": "LL.openeo_mapset_0.raster.S2A_B08_filter_daterange_NDVI_min_time",
          "rows": "2000",
          "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0",
          "title": "\"S2A_B08_filter_daterange_NDVI_min_time\""
        }


Ephemeral database approach
---------------------------

The second approach to use case 1 is to use ephemeral processing with the specification of an export process
to store the final NDVI raster layer into a cloud storage.

We create the process graph that uses a different approach and an export process at the end
as JSON code and send a POST API call via **curl** to the backend as a processing job:

   .. code-block:: json

        {
            "process_graph": {
                "process_id": "raster_exporter",
                "args": {
                    "collections": [{
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
                                                    "collections": [{"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"},
                                                                    {"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"}],
                                                    "bottom": 38.9,
                                                    "left": -4.8,
                                                    "right": -4.6,
                                                    "top": 39.1,
                                                    "ewres": 0.0001,
                                                    "nsres": 0.0001,
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
                    }]
                }
            }
        }

The JSON code must be stored in a shell variable and passed to the **curl** command:

   .. code-block:: bash

      JSON='{...}'

      curl -H "Content-Type: application/json" -X POST -d "${JSON}" http://openeo.mundialis.de:5000/jobs

   .. code-block:: json

        {
          "job_id": "resource_id-1d10265d-e435-4463-a913-e65e1a2cafe4",
          "job_info": {
            "accept_datetime": "2018-03-06 12:46:16.938811",
            "accept_timestamp": 1520340376.938808,
            "api_info": {
              "endpoint": "asyncephemeralexportgcsresource",
              "method": "POST",
              "path": "/locations/LL/processing_async_export_gcs",
              "request_url": "http://openeo.mundialis.de:8080/locations/LL/processing_async_export_gcs"
            },
            "datetime": "2018-03-06 12:46:16.940197",
            "http_code": 200,
            "message": "Resource accepted",
            "process_results": {},
            "resource_id": "resource_id-1d10265d-e435-4463-a913-e65e1a2cafe4",
            "status": "accepted",
            "time_delta": 0.0014121532440185547,
            "timestamp": 1520340376.940196,
            "urls": {
              "resources": [],
              "status": "http://openeo.mundialis.de:8080/status/user/resource_id-1d10265d-e435-4463-a913-e65e1a2cafe4"
            },
            "user_id": "user"
          }
        }

We need to poll for the final result using the job id, since the request is asynchronous:

   .. code-block:: bash

      curl -X GET http://openeo.mundialis.de:5000/jobs/resource_id-1d10265d-e435-4463-a913-e65e1a2cafe4

   .. code-block:: json

        {
          "consumed_credits": 53.54191303253174,
          "job_id": "resource_id-1d10265d-e435-4463-a913-e65e1a2cafe4",
          "job_info": {
            "accept_datetime": "2018-03-06 12:46:16.938811",
            "accept_timestamp": 1520340376.938808,
            "api_info": {
              "endpoint": "asyncephemeralexportgcsresource",
              "method": "POST",
              "path": "/locations/LL/processing_async_export_gcs",
              "request_url": "http://openeo.mundialis.de:8080/locations/LL/processing_async_export_gcs"
            },
            "datetime": "2018-03-06 12:47:10.480688",
            "http_code": 200,
            "message": "Processing successfully finished",
            "process_log": [
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.1",
                  "s=38.9",
                  "e=-4.6",
                  "w=-4.8",
                  "ewres=0.0001",
                  "nsres=0.0001"
                ],
                "return_code": 0,
                "run_time": 0.050132036209106445,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.1",
                  "s=38.9",
                  "e=-4.6",
                  "w=-4.8",
                  "ewres=0.0001",
                  "nsres=0.0001"
                ],
                "return_code": 0,
                "run_time": 0.05012989044189453,
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
                "run_time": 6.333992004394531,
                "stderr": [
                  "Default TGIS driver / database set to:",
                  "driver: sqlite",
                  "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite.db",
                  "WARNING: Temporal database connection defined as:",
                  "/graas/workspace/temp_db/gisdbase_89a821176c0b4702b36c27fe00575afc/LL/mapset_89a821176c0b4702b36c27fe00575afc/tgis/sqlite.db",
                  "But database file does not exist.",
                  "Creating temporal database: /graas/workspace/temp_db/gisdbase_89a821176c0b4702b36c27fe00575afc/LL/mapset_89a821176c0b4702b36c27fe00575afc/tgis/sqlite.db",
                  "0..0..100",
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
                "run_time": 6.443331003189087,
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
                "run_time": 7.3971569538116455,
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
                "run_time": 0.5798170566558838,
                "stderr": [
                  "Color table for raster map <ndvi_1@mapset_89a821176c0b4702b36c27fe00575afc> set to 'ndvi'",
                  "Color table for raster map <ndvi_2@mapset_89a821176c0b4702b36c27fe00575afc> set to 'ndvi'",
                  "Color table for raster map <ndvi_3@mapset_89a821176c0b4702b36c27fe00575afc> set to 'ndvi'",
                  "Color table for raster map <ndvi_4@mapset_89a821176c0b4702b36c27fe00575afc> set to 'ndvi'",
                  "Color table for raster map <ndvi_5@mapset_89a821176c0b4702b36c27fe00575afc> set to 'ndvi'",
                  "Color table for raster map <ndvi_6@mapset_89a821176c0b4702b36c27fe00575afc> set to 'ndvi'",
                  "Color table for raster map <ndvi_7@mapset_89a821176c0b4702b36c27fe00575afc> set to 'ndvi'",
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
                "run_time": 2.1993770599365234,
                "stderr": [
                  "0..3..6..9..12..15..18..21..24..27..30..33..36..39..42..45..48..51..54..57..60..63..66..69..72..75..78..81..84..87..90..93..96..99..100",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "r.out.gdal",
                "parameter": [
                  "-fm",
                  "input=S2A_B08_filter_daterange_NDVI_min_time",
                  "format=GTiff",
                  "createopt=COMPRESS=LZW",
                  "output=/graas/workspace/temp_db/gisdbase_89a821176c0b4702b36c27fe00575afc/.tmp/S2A_B08_filter_daterange_NDVI_min_time.tiff"
                ],
                "return_code": 0,
                "run_time": 0.7521610260009766,
                "stderr": [
                  "Checking GDAL data type and nodata value...",
                  "2..5..8..11..14..17..20..23..26..29..32..35..38..41..44..47..50..53..56..59..62..65..68..71..74..77..80..83..86..89..92..95..98..100",
                  "Using GDAL data type <Float64>",
                  "Exporting raster data to GTiff format...",
                  "ERROR 6: SetColorTable() only supported for Byte or UInt16 bands in TIFF format.",
                  "2..5..8..11..14..17..20..23..26..29..32..35..38..41..44..47..50..53..56..59..62..65..68..71..74..77..80..83..86..89..92..95..98..100",
                  "r.out.gdal complete. File </graas/workspace/temp_db/gisdbase_89a821176c0b4702b36c27fe00575afc/.tmp/S2A_B08_filter_daterange_NDVI_min_time.tiff> created.",
                  ""
                ],
                "stdout": ""
              }
            ],
            "process_results": {},
            "progress": {
              "num_of_steps": 8,
              "step": 8
            },
            "resource_id": "resource_id-1d10265d-e435-4463-a913-e65e1a2cafe4",
            "status": "finished",
            "time_delta": 53.54191303253174,
            "timestamp": 1520340430.480685,
            "urls": {
              "resources": [
                "https://storage.googleapis.com/graas-test-resources/user%2Fresource_id-1d10265d-e435-4463-a913-e65e1a2cafe4%2FS2A_B08_filter_daterange_NDVI_min_time.tiff?Expires=1521204430&GoogleAccessId=cloud-storage-admin%40eloquent-victor-483.iam.gserviceaccount.com&Signature=RcqtuaXW9a48wzuMt0Vj93dnj9CDCGJaIhtxCYj%2B0CkK2uZ4cS%2BI9yAA50HpG5hbWFd0If9BvIfvNYjvzEm8MaHFDXOVSqN8gxSOkcA7HpNN0lWvAdkL6OoOjeBiHO1MXjZy6lMxW7X8OGg8OaiEmCXt%2FJQwlSlazt5et8cfLeJ10K%2Ba6AZH3ngZm8yrBxgW%2BggT440h914i4kuTaR9j2ez1yHEovpOs%2BemN%2FGuQHZoGYid3z82MM3b8WhgZsuNO0nwcC2ttlZ4UL7iVZL2wW8nnlzfub1vS1eC4feO86YLsVwJqTo8%2BuzDPf%2BnljHN8WKYYK8p05IIXCkgs0p0naQ%3D%3D"
              ],
              "status": "http://openeo.mundialis.de:8080/status/user/resource_id-1d10265d-e435-4463-a913-e65e1a2cafe4"
            },
            "user_id": "user"
          },
          "last_update": "2018-03-06 12:47:10.480688",
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
                                  "collections": [
                                    {
                                      "args": {
                                        "bottom": 38.9,
                                        "collections": [
                                          {
                                            "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                          },
                                          {
                                            "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                                          }
                                        ],
                                        "ewres": 0.0001,
                                        "left": -4.8,
                                        "nsres": 0.0001,
                                        "right": -4.6,
                                        "srs": "EPSG:4326",
                                        "top": 39.1
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
                ]
              },
              "process_id": "raster_exporter"
            }
          },
          "resources": [
            "https://storage.googleapis.com/graas-test-resources/user%2Fresource_id-1d10265d-e435-4463-a913-e65e1a2cafe4%2FS2A_B08_filter_daterange_NDVI_min_time.tiff?Expires=1521204430&GoogleAccessId=cloud-storage-admin%40eloquent-victor-483.iam.gserviceaccount.com&Signature=RcqtuaXW9a48wzuMt0Vj93dnj9CDCGJaIhtxCYj%2B0CkK2uZ4cS%2BI9yAA50HpG5hbWFd0If9BvIfvNYjvzEm8MaHFDXOVSqN8gxSOkcA7HpNN0lWvAdkL6OoOjeBiHO1MXjZy6lMxW7X8OGg8OaiEmCXt%2FJQwlSlazt5et8cfLeJ10K%2Ba6AZH3ngZm8yrBxgW%2BggT440h914i4kuTaR9j2ez1yHEovpOs%2BemN%2FGuQHZoGYid3z82MM3b8WhgZsuNO0nwcC2ttlZ4UL7iVZL2wW8nnlzfub1vS1eC4feO86YLsVwJqTo8%2BuzDPf%2BnljHN8WKYYK8p05IIXCkgs0p0naQ%3D%3D"
          ],
          "status": "finished",
          "submitted": "2018-03-06 12:46:16.938811",
          "user_id": "user"
        }


The resulting NDVI raster layer is stored as GeoTiff file in the google cloud storage and can be accessed via and URL.

    .. image:: NDVI_minimum_use_case_1.png

openEO use case 2
=================

We modified use case two to process the previously created NDVI time series. The user defined function will
aggregate time by summing all values and produces a single raster layer.
The processing is run in an ephemeral database and the result will be exported by the exporter process as GeoTiff file.

The user defined function has the following code:

    .. code-block:: python

        import numpy as np

        def udf_time_series_to_raster_map(t):
            return np.sum(t["cell_array"], axis=0)
    ..

The function is located in a file that is accessible online

    https://storage.googleapis.com/datentransfer/aggr_func.py

The process graph looks as follows:

   .. code-block:: json

        {
            "process_graph": {
                "process_id": "raster_exporter",
                "args": {
                    "collections": [{
                        "process_id": "udf_reduce_time",
                        "args": {
                            "collections": [{
                                "process_id": "filter_daterange",
                                "args": {
                                    "collections": [{
                                        "process_id": "filter_bbox",
                                        "args": {
                                            "collections": [
                                                {"product_id": "LL.openeo_mapset_0.strds.S2A_B08_filter_daterange_NDVI"}],
                                             "bottom": 38.9,
                                             "left": -4.8,
                                             "right": -4.6,
                                             "top": 39.1,
                                             "ewres": 0.0001,
                                             "nsres": 0.0001,
                                             "srs": "EPSG:4326"
                                        }
                                    }],
                                    "from": "2017-04-12 11:17:08",
                                    "to": "2017-09-04 11:18:26"
                                }
                            }],
                            "python_file_url": "https://storage.googleapis.com/datentransfer/aggr_func.py"
                        }
                    }]
                }
            }
        }

The JSON code must be stored in a shell variable and passed to the **curl** command:

   .. code-block:: bash

      JSON='{...}'

      curl -H "Content-Type: application/json" -X POST -d "${JSON}" http://openeo.mundialis.de:5000/jobs

   .. code-block:: JSON

        {
          "job_id": "resource_id-d5d6ef2a-2a84-49a4-beea-d7514c90af74",
          "job_info": {
            "accept_datetime": "2018-03-06 13:06:38.036433",
            "accept_timestamp": 1520341598.036431,
            "api_info": {
              "endpoint": "asyncephemeralexportgcsresource",
              "method": "POST",
              "path": "/locations/LL/processing_async_export_gcs",
              "request_url": "http://openeo.mundialis.de:8080/locations/LL/processing_async_export_gcs"
            },
            "datetime": "2018-03-06 13:06:38.039900",
            "http_code": 200,
            "message": "Resource accepted",
            "process_results": {},
            "resource_id": "resource_id-d5d6ef2a-2a84-49a4-beea-d7514c90af74",
            "status": "accepted",
            "time_delta": 0.0034978389739990234,
            "timestamp": 1520341598.039899,
            "urls": {
              "resources": [],
              "status": "http://openeo.mundialis.de:8080/status/user/resource_id-d5d6ef2a-2a84-49a4-beea-d7514c90af74"
            },
            "user_id": "user"
          }
        }


   .. code-block:: bash

      curl -X GET http://openeo.mundialis.de:5000/jobs/resource_id-d5d6ef2a-2a84-49a4-beea-d7514c90af74

   .. code-block:: JSON

        {
          "consumed_credits": 43.888041973114014,
          "job_id": "resource_id-d5d6ef2a-2a84-49a4-beea-d7514c90af74",
          "job_info": {
            "accept_datetime": "2018-03-06 13:06:38.036433",
            "accept_timestamp": 1520341598.036431,
            "api_info": {
              "endpoint": "asyncephemeralexportgcsresource",
              "method": "POST",
              "path": "/locations/LL/processing_async_export_gcs",
              "request_url": "http://openeo.mundialis.de:8080/locations/LL/processing_async_export_gcs"
            },
            "datetime": "2018-03-06 13:07:21.924437",
            "http_code": 200,
            "message": "Processing successfully finished",
            "process_log": [
              {
                "executable": "/usr/bin/wget",
                "parameter": [
                  "-t5",
                  "-c",
                  "-q",
                  "-O",
                  "/graas/workspace/temp_db/gisdbase_ef7a7c01ba1d4715a8323c44aca9457b/.tmp/aggr_func.py",
                  "https://storage.googleapis.com/datentransfer/aggr_func.py"
                ],
                "return_code": 0,
                "run_time": 0.2505991458892822,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "/bin/mv",
                "parameter": [
                  "/graas/workspace/temp_db/gisdbase_ef7a7c01ba1d4715a8323c44aca9457b/.tmp/aggr_func.py",
                  "/graas/workspace/temp_db/gisdbase_ef7a7c01ba1d4715a8323c44aca9457b/.tmp/temp_file_1"
                ],
                "return_code": 0,
                "run_time": 0.050122976303100586,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.1",
                  "s=38.9",
                  "e=-4.6",
                  "w=-4.8",
                  "ewres=0.0001",
                  "nsres=0.0001"
                ],
                "return_code": 0,
                "run_time": 0.0501248836517334,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "t.rast.extract",
                "parameter": [
                  "input=S2A_B08_filter_daterange_NDVI@openeo_mapset_0",
                  "where=start_time >= '2017-04-12 11:17:08' AND end_time <= '2017-09-04 11:18:26'",
                  "output=S2A_B08_filter_daterange_NDVI_filter_daterange",
                  "expression=1.0 * S2A_B08_filter_daterange_NDVI@openeo_mapset_0",
                  "basename=S2A_B08_filter_daterange_NDVI_extract",
                  "suffix=num"
                ],
                "return_code": 0,
                "run_time": 5.497781991958618,
                "stderr": [
                  "Default TGIS driver / database set to:",
                  "driver: sqlite",
                  "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite.db",
                  "WARNING: Temporal database connection defined as:",
                  "/graas/workspace/temp_db/gisdbase_ef7a7c01ba1d4715a8323c44aca9457b/LL/mapset_ef7a7c01ba1d4715a8323c44aca9457b/tgis/sqlite.db",
                  "But database file does not exist.",
                  "Creating temporal database: /graas/workspace/temp_db/gisdbase_ef7a7c01ba1d4715a8323c44aca9457b/LL/mapset_ef7a7c01ba1d4715a8323c44aca9457b/tgis/sqlite.db",
                  "0..0..100",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "t.rast.aggr_func",
                "parameter": [
                  "pyfile=/graas/workspace/temp_db/gisdbase_ef7a7c01ba1d4715a8323c44aca9457b/.tmp/temp_file_1",
                  "input=S2A_B08_filter_daterange_NDVI_filter_daterange",
                  "output=S2A_B08_filter_daterange_NDVI_filter_daterange_udf_reduce_time"
                ],
                "return_code": 0,
                "run_time": 2.7383928298950195,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "r.out.gdal",
                "parameter": [
                  "-fm",
                  "input=S2A_B08_filter_daterange_NDVI_filter_daterange_udf_reduce_time",
                  "format=GTiff",
                  "createopt=COMPRESS=LZW",
                  "output=/graas/workspace/temp_db/gisdbase_ef7a7c01ba1d4715a8323c44aca9457b/.tmp/S2A_B08_filter_daterange_NDVI_filter_daterange_udf_reduce_time.tiff"
                ],
                "return_code": 0,
                "run_time": 0.8519728183746338,
                "stderr": [
                  "Checking GDAL data type and nodata value...",
                  "2..5..8..11..14..17..20..23..26..29..32..35..38..41..44..47..50..53..56..59..62..65..68..71..74..77..80..83..86..89..92..95..98..100",
                  "Using GDAL data type <Float64>",
                  "Exporting raster data to GTiff format...",
                  "ERROR 6: SetColorTable() only supported for Byte or UInt16 bands in TIFF format.",
                  "2..5..8..11..14..17..20..23..26..29..32..35..38..41..44..47..50..53..56..59..62..65..68..71..74..77..80..83..86..89..92..95..98..100",
                  "r.out.gdal complete. File </graas/workspace/temp_db/gisdbase_ef7a7c01ba1d4715a8323c44aca9457b/.tmp/S2A_B08_filter_daterange_NDVI_filter_daterange_udf_reduce_time.tiff> created.",
                  ""
                ],
                "stdout": ""
              }
            ],
            "process_results": {},
            "progress": {
              "num_of_steps": 6,
              "step": 6
            },
            "resource_id": "resource_id-d5d6ef2a-2a84-49a4-beea-d7514c90af74",
            "status": "finished",
            "time_delta": 43.888041973114014,
            "timestamp": 1520341641.924433,
            "urls": {
              "resources": [
                "https://storage.googleapis.com/graas-test-resources/user%2Fresource_id-d5d6ef2a-2a84-49a4-beea-d7514c90af74%2FS2A_B08_filter_daterange_NDVI_filter_daterange_udf_reduce_time.tiff?Expires=1521205641&GoogleAccessId=cloud-storage-admin%40eloquent-victor-483.iam.gserviceaccount.com&Signature=H9bk0yQyawKl5SNVB0cRXFgG7dKE8K%2F5wxlwjZB%2FjIRWYS4%2BzUfqH9LWQpmRJXTqrTvy%2F3m%2B3xkFz5LUyIUvQYTOePl5Sq3c%2B4J210LFCLiWW%2B17or7vZ0NMsD96xXzG7yzxs3GwjnFBYu%2FPdKBv8qBK0LtYzqyzMjEHMzOaquGEWP1eiOcMfWH%2B1xpEQ2sCz3SRS8gv6FEQ67vh19%2Fs22eewXvfhNpcYlHyP03iH0P814Sr8T8kMAAGEIqntMbHIMtetmqICfn%2FlRJ4m5nbHyg7DGddyVAQx8AzaA0cu1QMBXBmstQOHczVpQebG6%2FS7sdiDRDnHZVJbjG6lX%2Bpkg%3D%3D"
              ],
              "status": "http://openeo.mundialis.de:8080/status/user/resource_id-d5d6ef2a-2a84-49a4-beea-d7514c90af74"
            },
            "user_id": "user"
          },
          "last_update": "2018-03-06 13:07:21.924437",
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
                                  "bottom": 38.9,
                                  "collections": [
                                    {
                                      "product_id": "LL.openeo_mapset_0.strds.S2A_B08_filter_daterange_NDVI"
                                    }
                                  ],
                                  "ewres": 0.0001,
                                  "left": -4.8,
                                  "nsres": 0.0001,
                                  "right": -4.6,
                                  "srs": "EPSG:4326",
                                  "top": 39.1
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
                      "python_file_url": "https://storage.googleapis.com/datentransfer/aggr_func.py"
                    },
                    "process_id": "udf_reduce_time"
                  }
                ]
              },
              "process_id": "raster_exporter"
            }
          },
          "resources": [
            "https://storage.googleapis.com/graas-test-resources/user%2Fresource_id-d5d6ef2a-2a84-49a4-beea-d7514c90af74%2FS2A_B08_filter_daterange_NDVI_filter_daterange_udf_reduce_time.tiff?Expires=1521205641&GoogleAccessId=cloud-storage-admin%40eloquent-victor-483.iam.gserviceaccount.com&Signature=H9bk0yQyawKl5SNVB0cRXFgG7dKE8K%2F5wxlwjZB%2FjIRWYS4%2BzUfqH9LWQpmRJXTqrTvy%2F3m%2B3xkFz5LUyIUvQYTOePl5Sq3c%2B4J210LFCLiWW%2B17or7vZ0NMsD96xXzG7yzxs3GwjnFBYu%2FPdKBv8qBK0LtYzqyzMjEHMzOaquGEWP1eiOcMfWH%2B1xpEQ2sCz3SRS8gv6FEQ67vh19%2Fs22eewXvfhNpcYlHyP03iH0P814Sr8T8kMAAGEIqntMbHIMtetmqICfn%2FlRJ4m5nbHyg7DGddyVAQx8AzaA0cu1QMBXBmstQOHczVpQebG6%2FS7sdiDRDnHZVJbjG6lX%2Bpkg%3D%3D"
          ],
          "status": "finished",
          "submitted": "2018-03-06 13:06:38.036433",
          "user_id": "user"
        }

The resulting NDVI raster layer is stored as GeoTiff file in the google cloud storage and can be accessed via and URL.

    .. image:: NDVI_reduce_time_use_case_2.png


openEO use case 3
=================

The zonal statistics is based on the NDVI time series that was computed in the first use case and a polygon
that is publicly available as GeoJSON file in the google cloud storage.

The process graph has the following form:

   .. code-block:: JSON

        {
            "process_graph": {
                "process_id": "zonal_statistics",
                "args": {
                    "collections": [{
                        "process_id": "filter_daterange",
                        "args": {
                            "collections": [{
                                "process_id": "filter_bbox",
                                "args": {
                                    "collections": [
                                        {"product_id": "LL.openeo_mapset_0.strds.S2A_B08_filter_daterange_NDVI"}],
                                     "bottom": 38.9,
                                     "left": -4.8,
                                     "right": -4.6,
                                     "top": 39.1,
                                     "ewres": 0.0001,
                                     "nsres": 0.0001,
                                     "srs": "EPSG:4326"
                                }
                            }],
                            "from": "2017-04-12 11:17:08",
                            "to": "2017-09-04 11:18:26"
                        }
                    }],
                    "regions": "https://storage.googleapis.com/graas-geodata/roi_openeo_use_case_2.geojson"
                }
            }
        }

   .. code-block:: bash

      JSON='{...}'

      curl -H "Content-Type: application/json" -X POST -d "${JSON}" http://openeo.mundialis.de:5000/jobs

   .. code-block:: JSON

        {
          "job_id": "resource_id-a8694233-3daf-4549-87bd-aeee16bbb44e",
          "job_info": {
            "accept_datetime": "2018-03-06 13:32:48.580382",
            "accept_timestamp": 1520343168.580381,
            "api_info": {
              "endpoint": "asyncephemeralexportgcsresource",
              "method": "POST",
              "path": "/locations/LL/processing_async_export_gcs",
              "request_url": "http://openeo.mundialis.de:8080/locations/LL/processing_async_export_gcs"
            },
            "datetime": "2018-03-06 13:32:48.580963",
            "http_code": 200,
            "message": "Resource accepted",
            "process_results": {},
            "resource_id": "resource_id-a8694233-3daf-4549-87bd-aeee16bbb44e",
            "status": "accepted",
            "time_delta": 0.0005970001220703125,
            "timestamp": 1520343168.580963,
            "urls": {
              "resources": [],
              "status": "http://openeo.mundialis.de:8080/status/user/resource_id-a8694233-3daf-4549-87bd-aeee16bbb44e"
            },
            "user_id": "user"
          }
        }

   .. code-block:: bash

      curl -X GET http://openeo.mundialis.de:5000/jobs/resource_id-a8694233-3daf-4549-87bd-aeee16bbb44e

   .. code-block:: JSON

        {
          "consumed_credits": 9.396178007125854,
          "job_id": "resource_id-a8694233-3daf-4549-87bd-aeee16bbb44e",
          "job_info": {
            "accept_datetime": "2018-03-06 13:32:48.580382",
            "accept_timestamp": 1520343168.580381,
            "api_info": {
              "endpoint": "asyncephemeralexportgcsresource",
              "method": "POST",
              "path": "/locations/LL/processing_async_export_gcs",
              "request_url": "http://openeo.mundialis.de:8080/locations/LL/processing_async_export_gcs"
            },
            "datetime": "2018-03-06 13:32:57.976511",
            "http_code": 200,
            "message": "Processing successfully finished",
            "process_log": [
              {
                "executable": "/usr/bin/wget",
                "parameter": [
                  "-t5",
                  "-c",
                  "-q",
                  "-O",
                  "/graas/workspace/temp_db/gisdbase_6018e16171a642ac9c549543e98ecd28/.tmp/roi_openeo_use_case_2.geojson",
                  "https://storage.googleapis.com/graas-geodata/roi_openeo_use_case_2.geojson"
                ],
                "return_code": 0,
                "run_time": 0.25072813034057617,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "v.import",
                "parameter": [
                  "input=/graas/workspace/temp_db/gisdbase_6018e16171a642ac9c549543e98ecd28/.tmp/roi_openeo_use_case_2.geojson",
                  "output=polygon",
                  "--q"
                ],
                "return_code": 0,
                "run_time": 0.20058703422546387,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.1",
                  "s=38.9",
                  "e=-4.6",
                  "w=-4.8",
                  "ewres=0.0001",
                  "nsres=0.0001"
                ],
                "return_code": 0,
                "run_time": 0.0501561164855957,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "t.rast.extract",
                "parameter": [
                  "input=S2A_B08_filter_daterange_NDVI@openeo_mapset_0",
                  "where=start_time >= '2017-04-12 11:17:08' AND end_time <= '2017-09-04 11:18:26'",
                  "output=S2A_B08_filter_daterange_NDVI_filter_daterange",
                  "expression=1.0 * S2A_B08_filter_daterange_NDVI@openeo_mapset_0",
                  "basename=S2A_B08_filter_daterange_NDVI_extract",
                  "suffix=num"
                ],
                "return_code": 0,
                "run_time": 5.4537811279296875,
                "stderr": [
                  "Default TGIS driver / database set to:",
                  "driver: sqlite",
                  "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite.db",
                  "WARNING: Temporal database connection defined as:",
                  "/graas/workspace/temp_db/gisdbase_6018e16171a642ac9c549543e98ecd28/LL/mapset_6018e16171a642ac9c549543e98ecd28/tgis/sqlite.db",
                  "But database file does not exist.",
                  "Creating temporal database: /graas/workspace/temp_db/gisdbase_6018e16171a642ac9c549543e98ecd28/LL/mapset_6018e16171a642ac9c549543e98ecd28/tgis/sqlite.db",
                  "0..0..100",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "g.region",
                "parameter": [
                  "save=previous_region",
                  "-g"
                ],
                "return_code": 0,
                "run_time": 0.050247907638549805,
                "stderr": [
                  ""
                ],
                "stdout": "projection=3\nzone=0\nn=39.1\ns=38.9\nw=-4.8\ne=-4.6\nnsres=0.000100000000000001\newres=0.0001\nrows=2000\ncols=2000\ncells=4000000\n"
              },
              {
                "executable": "g.region",
                "parameter": [
                  "vector=polygon",
                  "-g"
                ],
                "return_code": 0,
                "run_time": 0.05015087127685547,
                "stderr": [
                  ""
                ],
                "stdout": "projection=3\nzone=0\nn=39.0685031847134\ns=38.9582484076433\nw=-4.76363057324841\ne=-4.65509554140127\nnsres=9.99590000635251e-05\newres=0.000100032287416717\nrows=1103\ncols=1085\ncells=1196755\n"
              },
              {
                "executable": "r.mask",
                "parameter": [
                  "vector=polygon"
                ],
                "return_code": 0,
                "run_time": 0.25061798095703125,
                "stderr": [
                  "Reading areas...",
                  "0..100",
                  "Writing raster map...",
                  "0..3..6..9..12..15..18..21..24..27..30..33..36..39..42..45..48..51..54..57..60..63..66..69..72..75..78..81..84..87..90..93..96..99..100",
                  "All subsequent raster operations will be limited to the MASK area. Removing or renaming raster map named 'MASK' will restore raster operations to normal.",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "t.rast.univar",
                "parameter": [
                  "input=S2A_B08_filter_daterange_NDVI_filter_daterange"
                ],
                "return_code": 0,
                "run_time": 1.662107229232788,
                "stderr": [
                  ""
                ],
                "stdout": "id|start|end|mean|min|max|mean_of_abs|stddev|variance|coeff_var|sum|null_cells|cells\nS2A_B08_filter_daterange_NDVI_extract_00001@mapset_6018e16171a642ac9c549543e98ecd28|2017-04-12 11:17:08|2017-04-12 11:17:09|0.487180515115657|-0.176594063639641|0.847264409065247|0.487222218958327|0.122021783969252|0.0148893157630388|25.0465238619578|413985.052983135|346998|1196755\nS2A_B08_filter_daterange_NDVI_extract_00002@mapset_6018e16171a642ac9c549543e98ecd28|2017-06-21 11:12:22|2017-06-21 11:12:23|0.272682572682767|-0.175438597798347|0.739982604980469|0.272710130061152|0.12807288474622|0.0164026638072185|46.9677557631147|231713.92491519|346998|1196755\nS2A_B08_filter_daterange_NDVI_extract_00003@mapset_6018e16171a642ac9c549543e98ecd28|2017-07-01 11:17:46|2017-07-01 11:17:47|0.279796613484412|-0.256611853837967|0.786031484603882|0.280093314065891|0.150831215086139|0.0227500554443612|53.9074484168274|237759.130884673|346998|1196755\nS2A_B08_filter_daterange_NDVI_extract_00004@mapset_6018e16171a642ac9c549543e98ecd28|2017-07-21 11:07:58|2017-07-21 11:07:59|0.271536718957628|-0.211125165224075|0.761948108673096|0.271582710360984|0.146195710546354|0.0213731857821532|53.8401256034793|230740.227691277|346998|1196755\nS2A_B08_filter_daterange_NDVI_extract_00005@mapset_6018e16171a642ac9c549543e98ecd28|2017-07-31 11:12:20|2017-07-31 11:12:21|0.256992564328118|-0.154771894216537|0.712555348873138|0.257010652196462|0.139074371349009|0.0193416807661222|54.1161070992874|218381.230485768|346998|1196755\nS2A_B08_filter_daterange_NDVI_extract_00006@mapset_6018e16171a642ac9c549543e98ecd28|2017-08-20 11:12:20|2017-08-20 11:12:21|0.235982454273365|-0.164585694670677|0.682393014431|0.236010567963981|0.132507392236182|0.0175582089972335|56.1513747469903|200527.742395972|346998|1196755\nS2A_B08_filter_daterange_NDVI_extract_00007@mapset_6018e16171a642ac9c549543e98ecd28|2017-09-04 11:18:25|2017-09-04 11:18:26|0.265493908824582|-0.310704946517944|0.72889769077301|0.265540178962243|0.15444445473479|0.0238530895983266|58.1725040015269|225605.30748105|346998|1196755\n"
              },
              {
                "executable": "r.mask",
                "parameter": [
                  "-r"
                ],
                "return_code": 0,
                "run_time": 0.15033602714538574,
                "stderr": [
                  "Raster MASK removed",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "g.region",
                "parameter": [
                  "region=previous_region",
                  "-g"
                ],
                "return_code": 0,
                "run_time": 0.05015110969543457,
                "stderr": [
                  ""
                ],
                "stdout": "projection=3\nzone=0\nn=39.1\ns=38.9\nw=-4.8\ne=-4.6\nnsres=0.000100000000000001\newres=0.0001\nrows=2000\ncols=2000\ncells=4000000\n"
              }
            ],
            "process_results": {},
            "progress": {
              "num_of_steps": 10,
              "step": 10
            },
            "resource_id": "resource_id-a8694233-3daf-4549-87bd-aeee16bbb44e",
            "status": "finished",
            "time_delta": 9.396178007125854,
            "timestamp": 1520343177.976506,
            "urls": {
              "resources": [],
              "status": "http://openeo.mundialis.de:8080/status/user/resource_id-a8694233-3daf-4549-87bd-aeee16bbb44e"
            },
            "user_id": "user"
          },
          "last_update": "2018-03-06 13:32:57.976511",
          "process_graph": {
            "process_graph": {
              "args": {
                "collections": [
                  {
                    "args": {
                      "collections": [
                        {
                          "args": {
                            "bottom": 38.9,
                            "collections": [
                              {
                                "product_id": "LL.openeo_mapset_0.strds.S2A_B08_filter_daterange_NDVI"
                              }
                            ],
                            "ewres": 0.0001,
                            "left": -4.8,
                            "nsres": 0.0001,
                            "right": -4.6,
                            "srs": "EPSG:4326",
                            "top": 39.1
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
                "regions": "https://storage.googleapis.com/graas-geodata/roi_openeo_use_case_2.geojson"
              },
              "process_id": "zonal_statistics"
            }
          },
          "resources": [],
          "status": "finished",
          "submitted": "2018-03-06 13:32:48.580382",
          "user_id": "user"
        }

The result is located in the job info field and can be converted into a table like:

+-------------------------------------------+-------------------+-------------------+-----------------+------------------+-----------------+-----------------+-----------------+------------------+----------------+----------------+----------+-------+
|id                                         |start              |end                |mean             |min               |max              |mean_of_abs      |stddev           |variance          |coeff_var       |sum             |null_cells|cells  |
+===========================================+===================+===================+=================+==================+=================+=================+=================+==================+================+================+==========+=======+
|S2A_B08_filter_daterange_NDVI_extract_00001|2017-04-12 11:17:08|2017-04-12 11:17:09|0.487180515115657|-0.176594063639641|0.847264409065247|0.487222218958327|0.122021783969252|0.0148893157630388|25.0465238619578|413985.052983135|346998    |1196755|
|S2A_B08_filter_daterange_NDVI_extract_00002|2017-06-21 11:12:22|2017-06-21 11:12:23|0.272682572682767|-0.175438597798347|0.739982604980469|0.272710130061152|0.12807288474622 |0.0164026638072185|46.9677557631147|231713.92491519 |346998    |1196755|
|S2A_B08_filter_daterange_NDVI_extract_00003|2017-07-01 11:17:46|2017-07-01 11:17:47|0.279796613484412|-0.256611853837967|0.786031484603882|0.280093314065891|0.150831215086139|0.0227500554443612|53.9074484168274|237759.130884673|346998    |1196755|
|S2A_B08_filter_daterange_NDVI_extract_00004|2017-07-21 11:07:58|2017-07-21 11:07:59|0.271536718957628|-0.211125165224075|0.761948108673096|0.271582710360984|0.146195710546354|0.0213731857821532|53.8401256034793|230740.227691277|346998    |1196755|
|S2A_B08_filter_daterange_NDVI_extract_00005|2017-07-31 11:12:20|2017-07-31 11:12:21|0.256992564328118|-0.154771894216537|0.712555348873138|0.257010652196462|0.139074371349009|0.0193416807661222|54.1161070992874|218381.230485768|346998    |1196755|
|S2A_B08_filter_daterange_NDVI_extract_00006|2017-08-20 11:12:20|2017-08-20 11:12:21|0.235982454273365|-0.164585694670677|0.682393014431   |0.236010567963981|0.132507392236182|0.0175582089972335|56.1513747469903|200527.742395972|346998    |1196755|
|S2A_B08_filter_daterange_NDVI_extract_00007|2017-09-04 11:18:25|2017-09-04 11:18:26|0.265493908824582|-0.310704946517944|0.72889769077301 |0.265540178962243|0.15444445473479 |0.0238530895983266|58.1725040015269|225605.30748105 |346998    |1196755|
+-------------------------------------------+-------------------+-------------------+-----------------+------------------+-----------------+-----------------+-----------------+------------------+----------------+----------------+----------+-------+



Contents
========

.. toctree::
   :maxdepth: 2

   License <license>
   Authors <authors>
   Changelog <changelog>
   Module Reference <api/modules>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
