# -*- coding: utf-8 -*-
from flask import json
import unittest
from openeo_grass_gis_driver.capabilities import CAPABILITIES, OUTPUT_FORMATS, SERVICE_TYPES
from openeo_grass_gis_driver.test_base import TestBase

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class CapabilitiesTestCase(TestBase):

    def test_capabilities(self):
        response = self.app.get('/')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         CAPABILITIES)

    def test_ouput_formats(self):
        response = self.app.get('/output_formats')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         OUTPUT_FORMATS)

    def test_service_types(self):
        response = self.app.get('/service_types')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         SERVICE_TYPES)


if __name__ == "__main__":
    unittest.main()
