# -*- coding: utf-8 -*-
from flask import json
import unittest
from openeo_grass_gis_driver.capabilities import CAPABILITIES, SERVICE_TYPES
from openeo_grass_gis_driver.jobs import OUTPUT_FORMATS
from openeo_grass_gis_driver.test_base import TestBase

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class CapabilitiesTestCase(TestBase):

    def test_capabilities(self):
        response = self.app.get('/', headers=self.auth)
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         CAPABILITIES)

    def test_ouput_formats(self):
        response = self.app.get('/output_formats', headers=self.auth)
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         OUTPUT_FORMATS)

    def test_service_types(self):
        response = self.app.get('/service_types', headers=self.auth)
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         SERVICE_TYPES)


if __name__ == "__main__":
    unittest.main()
