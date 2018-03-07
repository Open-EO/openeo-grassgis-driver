# -*- coding: utf-8 -*-
import unittest
from openeo_core.app import flask_api
from graas_openeo_core_wrapper.endpoints import create_endpoints
from graas_openeo_core_wrapper.config import Config as GRaaSConfig

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class TestBase(unittest.TestCase):

    create_endpoints()

    def setUp(self):
        self.app = flask_api.app.test_client()
        self.gconf = GRaaSConfig()
        self.gconf.PORT = "8080"
