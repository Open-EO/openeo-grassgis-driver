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

The test result should look like this:

    .. image:: OpenEO_GRaaS_Wrapper_Testsuite.png


7. Run the server:

   .. code-block:: bash

      python -m graas_openeo_core_wrapper.main

8. Get the swagger.json API description using curl:

   .. code-block:: bash

      curl -X GET http://localhost:5000/api/v0/swagger.json



================
openEO use cases
================

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

      curl http://127.0.0.1:5000/data/LL.sentinel2A_openeo_subset.strds.S2A_B08

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

      curl http://127.0.0.1:5000/processes

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

      curl http://127.0.0.1:5000/processes/raster_exporter

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

   .. code-block:: bash

      curl http://127.0.0.1:5000/processes/zonal_statistics

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

Use case one can be addressed in different ways using the eopenEO GRaaS wrapper. There are **POST** and **PUT**
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
                                          "bottom": 38.738166,
                                          "left": -5.333682,
                                          "right": -4.038089,
                                          "top": 39.745573,
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
                                              "bottom": 38.738166,
                                              "left": -5.333682,
                                              "right": -4.038089,
                                              "top": 39.745573,
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
                                          "collections": [{"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                          }],
                                          "bottom": 38.738166,
                                          "left": -5.333682,
                                          "right": -4.038089,
                                          "top": 39.745573,
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
                                              "bottom": 38.738166,
                                              "left": -5.333682,
                                              "right": -4.038089,
                                              "top": 39.745573,
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
      }'

   .. code-block:: bash

      curl -H "Content-Type: application/json" -X PUT -d "${JSON}" http://127.0.0.1:5000/jobs

   .. code-block:: json

        {
          "job_id": "resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153",
          "job_info": {
            "accept_datetime": "2018-03-06 09:30:51.638057",
            "accept_timestamp": 1520328651.638056,
            "api_info": {
              "endpoint": "asyncpersistentresource",
              "method": "POST",
              "path": "/locations/LL/mapsets/openeo_mapset_0/processing_async",
              "request_url": "http://localhost:8080/locations/LL/mapsets/openeo_mapset_0/processing_async"
            },
            "datetime": "2018-03-06 09:30:51.638687",
            "http_code": 200,
            "message": "Resource accepted",
            "process_results": {},
            "resource_id": "resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153",
            "status": "accepted",
            "time_delta": 0.0006520748138427734,
            "timestamp": 1520328651.638687,
            "urls": {
              "resources": [],
              "status": "http://localhost:8080/status/user/resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153"
            },
            "user_id": "user"
          }
        }


We need to poll for the final result using the job id, since the request is asynchronous:

   .. code-block:: bash

      curl -X GET http://127.0.0.1:5000/jobs/resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153

   .. code-block:: json

        {
          "consumed_credits": 55.61048603057861,
          "job_id": "resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153",
          "job_info": {
            "accept_datetime": "2018-03-06 09:30:51.638057",
            "accept_timestamp": 1520328651.638056,
            "api_info": {
              "endpoint": "asyncpersistentresource",
              "method": "POST",
              "path": "/locations/LL/mapsets/openeo_mapset_0/processing_async",
              "request_url": "http://localhost:8080/locations/LL/mapsets/openeo_mapset_0/processing_async"
            },
            "datetime": "2018-03-06 09:31:47.248490",
            "http_code": 200,
            "message": "Running executable t.rast.extract with parameters ['input=S2A_B04@sentinel2A_openeo_subset', \"where= ... subset', 'basename=S2A_B04_extract', 'suffix=num'] for 55.185 seconds",
            "progress": {
              "num_of_steps": 7,
              "step": 2
            },
            "resource_id": "resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153",
            "status": "running",
            "time_delta": 55.61048603057861,
            "timestamp": 1520328707.248487,
            "urls": {
              "resources": [],
              "status": "http://localhost:8080/status/user/resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153"
            },
            "user_id": "user"
          },
          "last_update": "2018-03-06 09:31:47.248490",
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
                                  "bottom": 38.738166,
                                  "collections": [
                                    {
                                      "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                    }
                                  ],
                                  "ewres": 0.0001,
                                  "left": -5.333682,
                                  "nsres": 0.0001,
                                  "right": -4.038089,
                                  "srs": "EPSG:4326",
                                  "top": 39.745573
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
                                  "bottom": 38.738166,
                                  "collections": [
                                    {
                                      "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                                    }
                                  ],
                                  "ewres": 0.0001,
                                  "left": -5.333682,
                                  "nsres": 0.0001,
                                  "right": -4.038089,
                                  "srs": "EPSG:4326",
                                  "top": 39.745573
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
          "submitted": "2018-03-06 09:30:51.638057",
          "user_id": "user"
        }

The final response will look like this:

   .. code-block:: bash

      curl -X GET http://127.0.0.1:5000/jobs/resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153

   .. code-block:: json

        {
          "consumed_credits": 537.8529329299927,
          "job_id": "resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153",
          "job_info": {
            "accept_datetime": "2018-03-06 09:30:51.638057",
            "accept_timestamp": 1520328651.638056,
            "api_info": {
              "endpoint": "asyncpersistentresource",
              "method": "POST",
              "path": "/locations/LL/mapsets/openeo_mapset_0/processing_async",
              "request_url": "http://localhost:8080/locations/LL/mapsets/openeo_mapset_0/processing_async"
            },
            "datetime": "2018-03-06 09:39:49.490957",
            "http_code": 200,
            "message": "Processing successfully finished",
            "process_log": [
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.745573",
                  "s=38.738166",
                  "e=-4.038089",
                  "w=-5.333682",
                  "ewres=0.0001",
                  "nsres=0.0001"
                ],
                "return_code": 0,
                "run_time": 0.0501708984375,
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
                "run_time": 111.82611799240112,
                "stderr": [
                  "Default TGIS driver / database set to:",
                  "driver: sqlite",
                  "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite.db",
                  "WARNING: Temporal database connection defined as:",
                  "/graas/workspace/temp_db/gisdbase_81866c70ef3047b3acf39bec798b4af8/LL/openeo_mapset_0/tgis/sqlite.db",
                  "But database file does not exist.",
                  "Creating temporal database: /graas/workspace/temp_db/gisdbase_81866c70ef3047b3acf39bec798b4af8/LL/openeo_mapset_0/tgis/sqlite.db",
                  "0..0..100",
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.745573",
                  "s=38.738166",
                  "e=-4.038089",
                  "w=-5.333682",
                  "ewres=0.0001",
                  "nsres=0.0001"
                ],
                "return_code": 0,
                "run_time": 0.05014801025390625,
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
                "run_time": 116.25619506835938,
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
                "run_time": 208.20145988464355,
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
                "run_time": 0.7015728950500488,
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
                "run_time": 51.971314907073975,
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
            "resource_id": "resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153",
            "status": "finished",
            "time_delta": 537.8529329299927,
            "timestamp": 1520329189.490954,
            "urls": {
              "resources": [],
              "status": "http://localhost:8080/status/user/resource_id-be560a9b-e50f-4b7a-9ff0-f35622f8f153"
            },
            "user_id": "user"
          },
          "last_update": "2018-03-06 09:39:49.490957",
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
                                  "bottom": 38.738166,
                                  "collections": [
                                    {
                                      "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                    }
                                  ],
                                  "ewres": 0.0001,
                                  "left": -5.333682,
                                  "nsres": 0.0001,
                                  "right": -4.038089,
                                  "srs": "EPSG:4326",
                                  "top": 39.745573
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
                                  "bottom": 38.738166,
                                  "collections": [
                                    {
                                      "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                                    }
                                  ],
                                  "ewres": 0.0001,
                                  "left": -5.333682,
                                  "nsres": 0.0001,
                                  "right": -4.038089,
                                  "srs": "EPSG:4326",
                                  "top": 39.745573
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
          "submitted": "2018-03-06 09:30:51.638057",
          "user_id": "user"
        }


Several raster time series datasets were produced in the process, that are now available. We show only the new generated
rime series and the resulting NDVI raster layer:

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
          "creation_time": "2018-03-06 09:38:08.251271",
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
          "mapset": "openeo_mapset_0",
          "max_max": "0.879587",
          "max_min": "0.806604",
          "min_max": "-0.500162",
          "min_min": "-0.866849",
          "modification_time": "2018-03-06 09:38:08.281240",
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

      curl http://127.0.0.1:5000/data/LL.openeo_mapset_0.raster.S2A_B08_filter_daterange_NDVI_min_time

   .. code-block:: json

        {
          "cells": "130518744",
          "cols": "12956",
          "comments": "\"r.series --overwrite file=\"/graas/workspace/temp_db/gisdbase_81866c7\\0ef3047b3acf39bec798b4af8/LL/openeo_mapset_0/.tmp/ba884fb4a052/43809\\.0\" output=\"S2A_B08_filter_daterange_NDVI_min_time\" method=\"minimum\"\\ quantile=\"",
          "datatype": "DCELL",
          "description": "Raster dataset",
          "ewres": "9.99994597097869e-05",
          "extent": {
            "bottom": 38.738166,
            "left": -5.333682,
            "right": -4.038089,
            "srs": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]\n",
            "top": 39.745573
          },
          "location": "LL",
          "mapset": "openeo_mapset_0",
          "nsres": "0.00010000069485805",
          "product_id": "LL.openeo_mapset_0.raster.S2A_B08_filter_daterange_NDVI_min_time",
          "rows": "10074",
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
                                                    "bottom": 38.738166,
                                                    "left": -5.333682,
                                                    "right": -4.038089,
                                                    "top": 39.745573,
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

      JSON='{
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
                                                    "bottom": 38.738166,
                                                    "left": -5.333682,
                                                    "right": -4.038089,
                                                    "top": 39.745573,
                                                    "ewres": 1.0001,
                                                    "nsres": 1.0001,
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
        }'

   .. code-block:: bash

      curl -H "Content-Type: application/json" -X POST -d "${JSON}" http://127.0.0.1:5000/jobs


We need to poll for the final result using the job id, since the request is asynchronous:

   .. code-block:: bash

      curl -X GET http://127.0.0.1:5000/jobs/resource_id-590e4217-e112-4ca4-9ad9-1448a169b80f

   .. code-block:: json

        {
          "consumed_credits": 1434.2429690361023,
          "job_id": "resource_id-590e4217-e112-4ca4-9ad9-1448a169b80f",
          "job_info": {
            "accept_datetime": "2018-03-06 09:49:50.293151",
            "accept_timestamp": 1520329790.29315,
            "api_info": {
              "endpoint": "asyncephemeralexportgcsresource",
              "method": "POST",
              "path": "/locations/LL/processing_async_export_gcs",
              "request_url": "http://localhost:8080/locations/LL/processing_async_export_gcs"
            },
            "datetime": "2018-03-06 10:13:44.536080",
            "http_code": 200,
            "message": "Processing successfully finished",
            "process_log": [
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.745573",
                  "s=38.738166",
                  "e=-4.038089",
                  "w=-5.333682",
                  "ewres=0.0001",
                  "nsres=0.0001"
                ],
                "return_code": 0,
                "run_time": 0.05018019676208496,
                "stderr": [
                  ""
                ],
                "stdout": ""
              },
              {
                "executable": "g.region",
                "parameter": [
                  "n=39.745573",
                  "s=38.738166",
                  "e=-4.038089",
                  "w=-5.333682",
                  "ewres=0.0001",
                  "nsres=0.0001"
                ],
                "return_code": 0,
                "run_time": 0.05013704299926758,
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
                "run_time": 111.74427103996277,
                "stderr": [
                  "Default TGIS driver / database set to:",
                  "driver: sqlite",
                  "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite.db",
                  "WARNING: Temporal database connection defined as:",
                  "/graas/workspace/temp_db/gisdbase_56055f58ba544010982ae8d6656ac892/LL/mapset_56055f58ba544010982ae8d6656ac892/tgis/sqlite.db",
                  "But database file does not exist.",
                  "Creating temporal database: /graas/workspace/temp_db/gisdbase_56055f58ba544010982ae8d6656ac892/LL/mapset_56055f58ba544010982ae8d6656ac892/tgis/sqlite.db",
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
                "run_time": 113.08110308647156,
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
                "run_time": 212.9360408782959,
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
                "run_time": 0.6519420146942139,
                "stderr": [
                  "Color table for raster map <ndvi_1@mapset_56055f58ba544010982ae8d6656ac892> set to 'ndvi'",
                  "Color table for raster map <ndvi_2@mapset_56055f58ba544010982ae8d6656ac892> set to 'ndvi'",
                  "Color table for raster map <ndvi_3@mapset_56055f58ba544010982ae8d6656ac892> set to 'ndvi'",
                  "Color table for raster map <ndvi_4@mapset_56055f58ba544010982ae8d6656ac892> set to 'ndvi'",
                  "Color table for raster map <ndvi_5@mapset_56055f58ba544010982ae8d6656ac892> set to 'ndvi'",
                  "Color table for raster map <ndvi_6@mapset_56055f58ba544010982ae8d6656ac892> set to 'ndvi'",
                  "Color table for raster map <ndvi_7@mapset_56055f58ba544010982ae8d6656ac892> set to 'ndvi'",
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
                "run_time": 52.439789056777954,
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
                  "output=/graas/workspace/temp_db/gisdbase_56055f58ba544010982ae8d6656ac892/.tmp/S2A_B08_filter_daterange_NDVI_min_time.tiff"
                ],
                "return_code": 0,
                "run_time": 22.20422601699829,
                "stderr": [
                  "Checking GDAL data type and nodata value...",
                  "2..5..8..11..14..17..20..23..26..29..32..35..38..41..44..47..50..53..56..59..62..65..68..71..74..77..80..83..86..89..92..95..98..100",
                  "Using GDAL data type <Float64>",
                  "Input raster map contains cells with NULL-value (no-data). The value -nan will be used to represent no-data values in the input map. You can specify a nodata value with the nodata option.",
                  "Exporting raster data to GTiff format...",
                  "ERROR 6: SetColorTable() only supported for Byte or UInt16 bands in TIFF format.",
                  "2..5..8..11..14..17..20..23..26..29..32..35..38..41..44..47..50..53..56..59..62..65..68..71..74..77..80..83..86..89..92..95..98..100",
                  "r.out.gdal complete. File </graas/workspace/temp_db/gisdbase_56055f58ba544010982ae8d6656ac892/.tmp/S2A_B08_filter_daterange_NDVI_min_time.tiff> created.",
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
            "resource_id": "resource_id-590e4217-e112-4ca4-9ad9-1448a169b80f",
            "status": "finished",
            "time_delta": 1434.2429690361023,
            "timestamp": 1520331224.536077,
            "urls": {
              "resources": [
                "https://storage.googleapis.com/graas-test-resources/user%2Fresource_id-590e4217-e112-4ca4-9ad9-1448a169b80f%2FS2A_B08_filter_daterange_NDVI_min_time.tiff?Expires=1521195224&GoogleAccessId=cloud-storage-admin%40eloquent-victor-483.iam.gserviceaccount.com&Signature=WJqxnVL7Bn54E6AqRvgukCjXGLW9Re8ri%2F0oWjaBSy5t7SabgJMQSmSnUHDM%2B4UB2FPPQ5253Mj%2FAc6wi2j7jVv4s6PZVDqwMnlOZC8Jt62NhirXc%2FJpZ03nhL%2BFt1u7AkhoYLynXLsI3Unok0BD%2FphzajZj3nbfBxCcHrZ4QE0VmwoBuWjww1ZexXUz%2FTYII9SDw2RkvHZR5mNq9T77ZyX8rQ%2FHtYIvtHgo2PK01pH8v%2Bx%2Fo8VzMb8eXh7FwAOMJnM9x0WL8eHHOuv%2Bf9WhcomaMj1xoPguDbrCiq7rlrxInHXBRBaYwRQWYj7LxPRPNhW6%2BbVf2fve9SKvEwYMsw%3D%3D"
              ],
              "status": "http://localhost:8080/status/user/resource_id-590e4217-e112-4ca4-9ad9-1448a169b80f"
            },
            "user_id": "user"
          },
          "last_update": "2018-03-06 10:13:44.536080",
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
                                        "bottom": 38.738166,
                                        "collections": [
                                          {
                                            "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                          },
                                          {
                                            "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                                          }
                                        ],
                                        "ewres": 0.0001,
                                        "left": -5.333682,
                                        "nsres": 0.0001,
                                        "right": -4.038089,
                                        "srs": "EPSG:4326",
                                        "top": 39.745573
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
            "https://storage.googleapis.com/graas-test-resources/user%2Fresource_id-590e4217-e112-4ca4-9ad9-1448a169b80f%2FS2A_B08_filter_daterange_NDVI_min_time.tiff?Expires=1521195224&GoogleAccessId=cloud-storage-admin%40eloquent-victor-483.iam.gserviceaccount.com&Signature=WJqxnVL7Bn54E6AqRvgukCjXGLW9Re8ri%2F0oWjaBSy5t7SabgJMQSmSnUHDM%2B4UB2FPPQ5253Mj%2FAc6wi2j7jVv4s6PZVDqwMnlOZC8Jt62NhirXc%2FJpZ03nhL%2BFt1u7AkhoYLynXLsI3Unok0BD%2FphzajZj3nbfBxCcHrZ4QE0VmwoBuWjww1ZexXUz%2FTYII9SDw2RkvHZR5mNq9T77ZyX8rQ%2FHtYIvtHgo2PK01pH8v%2Bx%2Fo8VzMb8eXh7FwAOMJnM9x0WL8eHHOuv%2Bf9WhcomaMj1xoPguDbrCiq7rlrxInHXBRBaYwRQWYj7LxPRPNhW6%2BbVf2fve9SKvEwYMsw%3D%3D"
          ],
          "status": "finished",
          "submitted": "2018-03-06 09:49:50.293151",
          "user_id": "user"
        }

The resulting NDVI raster layer is stored as GeoTiff file in the google cloud storage and can be accessed via and URL.

    .. image:: NDVI_minimum_use_case_1.png

openEO use case 2
=================

We modified use case two to process the previously created NDVI time series. The user defined function will
aggregate time and produces a single raster layer. The processing is run in an ephemeral database and the result
will be exported by the exporter process as GeoTiff file.

The process graph looks as follows:

   .. code-block:: json




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
