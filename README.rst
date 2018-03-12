========================
The GRaaS openEO wrapper
========================

This software implements the openEO Core API interface for the GRASS GIS as a Service (GRaaS) software solution
for parallel, large scale geodata processing.
GRaaS is a highly scalable open source REST interface to process geodata with the GRASS GIS in a distributed environment.

What is openEO?

    openEO - A Common, Open Source Interface between Earth Observation Data Infrastructures
    and Front-End Applications is an H2020 project funded under call EO-2-2017:
    EO Big Data Shift, under grant number 776242. The project runs from Oct 2017 to Sept 2020.

    https://openeo.org/

This document demonstrates the application of the openEO GRaaS wrapper to solve the three use cases
that were defined by the development group for the first prototype.

    https://open-eo.github.io/openeo-api-poc/poc/index.html#proof-of-concept


Installation
============

1. Deploy the GRaaS installation using docker.

2. Deploy the openEO GRaaS wrapper locally:

    1. Make sure to deploy the GRASS GIS locations that are required for the GRaaS openEO wrapper test suite
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
       ..

    2. Create directory that should contain the code and the virtual environment and switch the environment.
       It is preferred to run the openEO GRaaS wrapper in a virtual python environment:

       .. code-block:: bash

          mkdir openEO
          cd openEO
          virtualenv -p python3.5 venv
          source venv/bin/activate
       ..

    3. Clone the official openEO reference implementation repository and install
       the required Python packages into the virtual environment:

       .. code-block:: bash

          git clone https://bitbucket.org/huhabla/openeo_core.git openeo_core
          cd openeo_core
          pip install -r requirements.txt
          python setup.py install
       ..

    4. After installing the official openEO reference implementation, the GRaaS
       openEO wrapper must be installed, since it is based on the reference implementation.

       .. code-block:: bash

          git clone https://bitbucket.org/huhabla/graas_openeo_core_wrapper.git graas_openeo_core_wrapper
          cd graas_openeo_core_wrapper
          pip install -r requirements.txt
          python setup.py install
       ..

    5. Run the GRaaS openEO Core API test suite:

       .. code-block:: bash

          python setup.py test
       ..

    6. Run the server locally:

       .. code-block:: bash

          python -m graas_openeo_core_wrapper.main
       ..

8. Alternatively use the docker deployment located in the **docker** directory of this repository

    1. Make sure the GRaaS deployment is reachable by the openEO GRaaS wrapper container
    2. use the **build.sh** in the **docker** directory to build the image
    3. Deploy the openEO GRaaS docker container

        .. code-block:: bash

            cd graas_openeo_core_wrapper/docker
            docker build -t graas_openeo_core_wrapper .
            docker run --name=graas_wrapper -p 5000:5000 graas_openeo_core_wrapper
        ..

9. Get the swagger.json API description using curl:

   .. code-block:: bash

      curl -X GET http://openeo.mundialis.de:5000/api/v0/swagger.json

10. Explore the capabilities, data and processes that are available:

   .. code-block:: bash

      curl http://openeo.mundialis.de:5000/capabilities
      curl http://openeo.mundialis.de:5000/data
      curl http://openeo.mundialis.de:5000/processes
