========================
The GRaaS openEO wrapper
========================

This software implements the openEO Core API interface above the GRASS GIS as a Service (GRaaS) solution.
GRaaS is a REST interface to process geodata with the GRASS GIS.


Installation
============

Make sure to deploy the GRASS GIS locations that are required for the GRaaS openEO wrapper test suite
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

Deploy the GRaaS installation using docker.

It is preferred to run the openEO GRaaS wrapper in a virtual python environment.

Create directory that should contain the code and the virtual environment and switch the environment:

   .. code-block:: bash

      mkdir openEO
      cd openEO
      virtualenv -p python3.5 venv
      source venv/bin/activate

Clone the official openEO reference implementation
repository and install the required Python packages into the virtual environment:

   .. code-block:: bash

      git clone https://bitbucket.org/huhabla/openeo_core.git openeo_core
      cd openeo_core
      pip install -r requirements.txt
      python setup.py install

After installing the official openEO reference implementation
the GRaaS openEO wrapper must be installed, since it is based on the reference implementation.

   .. code-block:: bash

      git clone https://bitbucket.org/huhabla/graas_openeo_core_wrapper.git graas_openeo_core_wrapper
      cd graas_openeo_core_wrapper
      pip install -r requirements.txt
      python setup.py install

Run the GRaaS openEO Core API test suite:

   .. code-block:: bash

      python setup.py test

Run the test server:

   .. code-block:: bash

      python -m graas_openeo_core_wrapper.main

Get the swagger.json API description using curl:

   .. code-block:: bash

      curl -X GET http://localhost:5000/api/v0/swagger.json

    style.

Perform the openEO use cases:

   .. code-block:: bash


List available data

   .. code-block:: bash

      curl http://127.0.0.1:5000/data

      # Result

      [
        {
          "description": "Space time raster dataset",
          "product_id": "S2A_B04@sentinel2A_openeo_subset",
          "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset"
        },
        {
          "description": "Space time raster dataset",
          "product_id": "S2A_B08@sentinel2A_openeo_subset",
          "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset"
        }
      ]


Get information about band 04 of the sentinel2a  time series

   .. code-block:: bash

      curl http://127.0.0.1:5000/data/S2A_B04@sentinel2A_openeo_subset

      # Result

      {
        "aggregation_type": "None",
        "bands": {
          "band_id": "S2A_B04@sentinel2A_openeo_subset"
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
        "map_time": "interval",
        "mapset": "sentinel2A_openeo_subset",
        "max_max": "22259.0",
        "max_min": "13773.0",
        "min_max": "0.0",
        "min_min": "0.0",
        "modification_time": "2018-02-13 23:43:43.126555",
        "number_of_maps": "7",
        "product_id": "S2A_B04@sentinel2A_openeo_subset",
        "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset",
        "temporal_type": "2017-04-12 11:17:08",
        "time": {
          "from": "2017-04-12 11:17:08",
          "to": "2017-09-04 11:18:26"
        }
      }


Get information about band 08 of the sentinel2a  time series

   .. code-block:: bash

      curl http://127.0.0.1:5000/data/S2A_B08@sentinel2A_openeo_subset

      # Result

      {
        "aggregation_type": "None",
        "bands": {
          "band_id": "S2A_B08@sentinel2A_openeo_subset"
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
        "map_time": "interval",
        "mapset": "sentinel2A_openeo_subset",
        "max_max": "23033.0",
        "max_min": "20256.0",
        "min_max": "0.0",
        "min_min": "0.0",
        "modification_time": "2018-02-13 23:43:44.111735",
        "number_of_maps": "7",
        "product_id": "S2A_B08@sentinel2A_openeo_subset",
        "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset",
        "temporal_type": "2017-04-12 11:17:08",
        "time": {
          "from": "2017-04-12 11:17:08",
          "to": "2017-09-04 11:18:26"
        }
      }


List process information about all processes that are available for computation

   .. code-block:: bash

      curl http://127.0.0.1:5000/processes

      [
        "udf_reduce_time",
        "min_time",
        "NDVI",
        "filter_daterange",
        "filter_bbox"
      ]


Get information about each available process

   .. code-block:: bash

      curl http://127.0.0.1:5000/processes/udf_reduce_time

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

      curl http://127.0.0.1:5000/processes/min_time

      {
        "args": {
          "collections": {
            "description": "array of input collections with one element"
          }
        },
        "description": "Finds the minimum value of time series for all bands of the input dataset.",
        "process_id": "min_time"
      }

      curl http://127.0.0.1:5000/processes/NDVI

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

      curl http://127.0.0.1:5000/processes/filter_daterange

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


      curl http://127.0.0.1:5000/processes/filter_bbox

      {
        "args": {
          "bottom": {
            "description": "bottom boundary (latitude / northing)"
          },
          "collections": {
            "description": "array of input collections with one element"
          },
          "left": {
            "description": "left boundary (longitude / easting)"
          },
          "right": {
            "description": "right boundary (longitude / easting)"
          },
          "srs": {
            "description": "spatial reference system of boundaries as proj4 or EPSG:12345 like string"
          },
          "top": {
            "description": "top boundary (latitude / northing)"
          }
        },
        "description": "Drops observations from a collection that are located outside of a given bounding box.",
        "process_id": "filter_bbox"
      }

Create the use case 1 job


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
                                              "product_id": "S2A_B04@sentinel2A_openeo_subset"
                                          }],
                                          "left": -5.0,
                                          "right": -4.98,
                                          "top": 39.12,
                                          "bottom": 39.1,
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
                                                  "product_id": "S2A_B08@sentinel2A_openeo_subset"
                                              }],
                                              "left": -5.0,
                                              "right": -4.98,
                                              "top": 39.12,
                                              "bottom": 39.1,
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

      curl -H "Content-Type: application/json" -X POST -d "${JSON}" http://127.0.0.1:5000/jobs

      {
        "job_id": "resource_id-ca37a2ca-95ff-42c2-b6bd-15aa5ee7b5f0",
        "job_info": {
          "accept_datetime": "2018-03-02 10:24:54.871719",
          "accept_timestamp": 1519986294.871718,
          "api_info": {
            "endpoint": "asyncpersistentresource",
            "method": "POST",
            "path": "/locations/LL/mapsets/openeo_mapset_0/processing_async",
            "request_url": "http://localhost:8080/locations/LL/mapsets/openeo_mapset_0/processing_async"
          },
          "datetime": "2018-03-02 10:24:54.872517",
          "http_code": 200,
          "message": "Resource accepted",
          "process_results": {},
          "resource_id": "resource_id-ca37a2ca-95ff-42c2-b6bd-15aa5ee7b5f0",
          "status": "accepted",
          "time_delta": 0.0008151531219482422,
          "timestamp": 1519986294.872516,
          "urls": {
            "resources": [],
            "status": "http://localhost:8080/status/user/resource_id-ca37a2ca-95ff-42c2-b6bd-15aa5ee7b5f0"
          },
          "user_id": "user"
        }
      }

We need to poll for the final result, since the request is asynchronous using the job id:

   .. code-block:: bash

      curl -X GET http://127.0.0.1:5000/jobs/resource_id-ca37a2ca-95ff-42c2-b6bd-15aa5ee7b5f0

      # Result

      {
        "consumed_credits": 4.009669065475464,
        "job_id": "resource_id-ca37a2ca-95ff-42c2-b6bd-15aa5ee7b5f0",
        "job_info": {
          "accept_datetime": "2018-03-02 10:24:54.871719",
          "accept_timestamp": 1519986294.871718,
          "api_info": {
            "endpoint": "asyncpersistentresource",
            "method": "POST",
            "path": "/locations/LL/mapsets/openeo_mapset_0/processing_async",
            "request_url": "http://localhost:8080/locations/LL/mapsets/openeo_mapset_0/processing_async"
          },
          "datetime": "2018-03-02 10:24:58.881357",
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
                "ewres=0.0001",
                "nsres=0.0001"
              ],
              "return_code": 0,
              "run_time": 0.05009889602661133,
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
              "run_time": 0.9373860359191895,
              "stderr": [
                "Default TGIS driver / database set to:",
                "driver: sqlite",
                "database: $GISDBASE/$LOCATION_NAME/$MAPSET/tgis/sqlite.db",
                "WARNING: Temporal database connection defined as:",
                "/graas/workspace/temp_db/gisdbase_7efed75dba8a4acbb77a6f7eafead8e8/LL/openeo_mapset_0/tgis/sqlite.db",
                "But database file does not exist.",
                "Creating temporal database: /graas/workspace/temp_db/gisdbase_7efed75dba8a4acbb77a6f7eafead8e8/LL/openeo_mapset_0/tgis/sqlite.db",
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
                "ewres=0.0001",
                "nsres=0.0001"
              ],
              "return_code": 0,
              "run_time": 0.05010199546813965,
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
              "run_time": 0.9021859169006348,
              "stderr": [
                "0..0..100",
                ""
              ],
              "stdout": ""
            },
            {
              "executable": "t.rast.mapcalc",
              "parameter": [
                "expression=S2A_B04_filter_daterange_NDVI = float((S2A_B08_filter_daterange - S2A_B04_filter_daterange)/(S2A_B08_filter_daterange + S2A_B04_filter_daterange))",
                "inputs=S2A_B08_filter_daterange,S2A_B04_filter_daterange",
                "basename=ndvi",
                "output=S2A_B04_filter_daterange_NDVI"
              ],
              "return_code": 0,
              "run_time": 0.701524019241333,
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
                "input=S2A_B04_filter_daterange_NDVI",
                "color=ndvi"
              ],
              "return_code": 0,
              "run_time": 0.5119709968566895,
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
                "input=S2A_B04_filter_daterange_NDVI",
                "method=minimum",
                "output=S2A_B04_filter_daterange_NDVI_min_time",
                "-t"
              ],
              "return_code": 0,
              "run_time": 0.4966621398925781,
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
          "resource_id": "resource_id-ca37a2ca-95ff-42c2-b6bd-15aa5ee7b5f0",
          "status": "finished",
          "time_delta": 4.009669065475464,
          "timestamp": 1519986298.881355,
          "urls": {
            "resources": [],
            "status": "http://localhost:8080/status/user/resource_id-ca37a2ca-95ff-42c2-b6bd-15aa5ee7b5f0"
          },
          "user_id": "user"
        },
        "last_update": "2018-03-02 10:24:58.881357",
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
                                    "product_id": "S2A_B04@sentinel2A_openeo_subset"
                                  }
                                ],
                                "left": -5.0,
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
                                    "product_id": "S2A_B08@sentinel2A_openeo_subset"
                                  }
                                ],
                                "left": -5.0,
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
        "submitted": "2018-03-02 10:24:54.871719",
        "user_id": "user"
      }

Several raster time series datasets were produced in the process, that are now available:

   .. code-block:: bash

      curl http://127.0.0.1:5000/data

      # Result

      [
        {
          "description": "Space time raster dataset",
          "product_id": "S2A_B04_filter_daterange@openeo_mapset_0",
          "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0"
        },
        {
          "description": "Space time raster dataset",
          "product_id": "S2A_B04_filter_daterange_NDVI@openeo_mapset_0",
          "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0"
        },
        {
          "description": "Space time raster dataset",
          "product_id": "S2A_B08_filter_daterange@openeo_mapset_0",
          "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0"
        },
        {
          "description": "Space time raster dataset",
          "product_id": "S2A_B04@sentinel2A_openeo_subset",
          "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset"
        },
        {
          "description": "Space time raster dataset",
          "product_id": "S2A_B08@sentinel2A_openeo_subset",
          "source": "GRASS GIS location/mapset path: /LL/sentinel2A_openeo_subset"
        }
      ]

We inspect the new time series

   .. code-block:: bash

      curl http://127.0.0.1:5000/data/S2A_B04_filter_daterange_NDVI@openeo_mapset_0

      # Result

      {
        "aggregation_type": "None",
        "bands": {
          "band_id": "S2A_B04_filter_daterange_NDVI@openeo_mapset_0"
        },
        "creation_time": "2018-03-02 10:24:57.728966",
        "description": "Space time raster dataset",
        "extent": {
          "bottom": 39.1,
          "left": -5.0,
          "right": -4.98,
          "srs": "GEOGCS[\"WGS 84\",DATUM[\"WGS_1984\",SPHEROID[\"WGS 84\",6378137,298.257223563,AUTHORITY[\"EPSG\",\"7030\"]],AUTHORITY[\"EPSG\",\"6326\"]],PRIMEM[\"Greenwich\",0,AUTHORITY[\"EPSG\",\"8901\"]],UNIT[\"degree\",0.0174532925199433,AUTHORITY[\"EPSG\",\"9122\"]],AUTHORITY[\"EPSG\",\"4326\"]]\n",
          "top": 39.12
        },
        "granularity": "1 second",
        "map_time": "interval",
        "mapset": "openeo_mapset_0",
        "max_max": "0.776141",
        "max_min": "0.606734",
        "min_max": "-0.09617",
        "min_min": "-0.267157",
        "modification_time": "2018-03-02 10:24:57.746467",
        "number_of_maps": "7",
        "product_id": "S2A_B04_filter_daterange_NDVI@openeo_mapset_0",
        "source": "GRASS GIS location/mapset path: /LL/openeo_mapset_0",
        "temporal_type": "2017-04-12 11:17:08",
        "time": {
          "from": "2017-04-12 11:17:08",
          "to": "2017-09-04 11:18:26"
        }
      }


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
