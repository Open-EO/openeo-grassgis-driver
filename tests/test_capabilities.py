# -*- coding: utf-8 -*-
from flask import json
import unittest
from openeo_grass_gis_driver.capabilities import ACTINIA_CAPABILITIES
from openeo_grass_gis_driver.test_base import TestBase

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class CapabilitiesTestCase(TestBase):

    def test_capabilities(self):
        response = self.app.get('/capabilities')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         ACTINIA_CAPABILITIES)


if __name__ == "__main__":
    unittest.main()
