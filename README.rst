===========================
The OpenEO GRASS GIS driver
===========================

This software implements the openEO Core API interface for the GRASS GIS as a Service (GRaaS) software solution
for parallel, large scale geodata processing.
GRaaS is a highly scalable open source REST interface to process geodata with the GRASS GIS in a distributed environment.
It is deployed on **openeo.mundialis.de** and will be used for processing all openEO API calls taht are send to
the te OpenEO GRASS GIS driver.

What is openEO?

    openEO - A Common, Open Source Interface between Earth Observation Data Infrastructures
    and Front-End Applications is an H2020 project funded under call EO-2-2017:
    EO Big Data Shift, under grant number 776242. The project runs from Oct 2017 to Sept 2020.

    http://openeo.org/

This document demonstrates the application of the openEO GRaaS wrapper to solve the three use cases
that were defined by the development group for the first prototype.

    https://open-eo.github.io/openeo-api/poc/index.html#proof-of-concept


Installation
============

An active internet connection is required. All requests to the openEO GRASS GIS driver will be send and processed on the **openeo.mundialis.de** server.

1. Deploy the openEO GRASS GIS driver locally:

    1. Create directory that should contain the code and the virtual environment and switch the environment.
       It is preferred to run the openEO GRaaS wrapper in a virtual python environment:

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
