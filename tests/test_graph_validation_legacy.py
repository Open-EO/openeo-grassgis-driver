# -*- coding: utf-8 -*-
import unittest
from flask import json
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.utils.process_graph_examples_legacy import ndvi_1, filter_bbox, openeo_usecase_1

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GraphValidationTestCase(TestBase):

    def test_1_graph_filter_bbox_nc(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(filter_bbox), content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_2_graph_ndvi(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(ndvi_1), content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_3_use_case_1(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(openeo_usecase_1), content_type="application/json")
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
