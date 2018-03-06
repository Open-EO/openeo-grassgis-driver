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
