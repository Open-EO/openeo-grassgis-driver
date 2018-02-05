=============================
GRaaS openEO Core API wrapper
=============================

This is the GRaaS openEO Core API wrapper that uses the oopenEO reference implementation Python package to
implement the openEO API functionality.


Description
===========

This software implements the openEO core API definition and uses the GRaaS functionality
as backend. It is a wrapper around GRaaS and requires a running GRaaS infrastructure
to run.


Installation
============

The openEO Core API reference implementation and a running GRaaS infrastructure is required to run this wrapper.

It is preferred to run the GRaaS openEO Core API wrapper in a virtual python environment.

Create directory that contains the code and the virtual environment and switch the environment:

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

