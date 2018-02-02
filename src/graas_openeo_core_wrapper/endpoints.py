# -*- coding: utf-8 -*-
from openeo_core.app import flask_api
from graas_openeo_core_wrapper.capabilities import GRaaSCapabilities

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def create_endpoints():
    """Create all endpoints for the openEO Core API GRaaS wrapper

    :return:
    """
    flask_api.add_resource(GRaaSCapabilities, '/capabilities')
