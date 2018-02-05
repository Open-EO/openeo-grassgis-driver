=============================
GRaaS openEO Core API wrapper
=============================

This is the GRaaS openEO Core API wrapper.

Description
===========

This software implements the openEO core API definition and uses GRASS GIS as a Service (GRaaS)
as backend. It is a wrapper around GRaaS REST API and requires a running GRaaS infrastructure.


Installation
============

The openEO Core API reference implementation must be installed to run the wrapper.

It is preferred to run the openEO Core API and the GRaaS openEO Core API wrapper together
in a virtual python environment.

Create directory that contains the code and the virtual environment of booth frameworks
and switch the environment:

    .. code-block:: bash

        mkdir openEO
        cd openEO
        virtualenv -p python3.5 venv
        source venv/bin/activate

Clone the official repositories of the openEO reference implementation and the GRaaS wrapper.
Install the required Python packages into the virtual environment:

    .. code-block:: bash

        git clone https://bitbucket.org/huhabla/openeo_core.git openeo_core
        cd openeo_core
        pip install -r requirements.txt
        python setup.py install

        cd -

        git clone https://bitbucket.org/huhabla/graas_openeo_core_wrapper.git graas_openeo_core_wrapper
        cd graas_openeo_core_wrapper
        pip install -r requirements.txt
        python setup.py install

Run the GRaaS openEO Core API wrapper test suite:

    .. code-block::

        python setup.py test

Run the test server:

    .. code-block:: bash

        python -m graas_openeo_core_wrapper.main

Get the swagger.json API description using curl:

    .. code-block:: bash

        curl -X GET http://localhost:5000/api/v0/swagger.json

