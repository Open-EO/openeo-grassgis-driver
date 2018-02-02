# -*- coding: utf-8 -*-
import json
import sys
import unittest
from openeo_core.app import flask_api
from graas_openeo_core_wrapper.capabilities import GRAAS_CAPABILITIES
from graas_openeo_core_wrapper.endpoints import create_endpoints
from graas_openeo_core_wrapper.graas_wrapper import GRaaSInterface
from graas_openeo_core_wrapper.config import Config as GRaaSConfig

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class AllTestCase(unittest.TestCase):

    create_endpoints()

    def setUp(self):
        self.app = flask_api.app.test_client()
        self.gconf = GRaaSConfig()
        self.gconf.PORT = "8080"


    def test_capabilities(self):
        response = self.app.get('/capabilities')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         GRAAS_CAPABILITIES)

    def test_health_check(self):

        iface = GRaaSInterface(self.gconf)
        self.assertTrue(iface.check_health())

    def test_list_raster(self):

        iface = GRaaSInterface(self.gconf)
        raster = iface.list_raster()
        print(raster)


if __name__ == "__main__":
    unittest.main()
