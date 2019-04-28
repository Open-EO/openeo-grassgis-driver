# -*- coding: utf-8 -*-
import pprint
import unittest
from flask import json
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.utils.process_graph_examples_v04 import *

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GraphValidationTestCase(TestBase):

    def test_1_graph_filter_bbox(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(FILTER_BBOX), content_type="application/json", headers=self.auth)
        self.assertEqual(response.status_code, 204)

    def test_2_graph_ndvi(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(NDVI_STRDS), content_type="application/json", headers=self.auth)
        self.assertEqual(response.status_code, 204)

    def test_3_graph_get_data_1(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(GET_DATA_1), content_type="application/json", headers=self.auth)
        self.assertEqual(response.status_code, 204)

    def test_4_graph_get_data_3(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(GET_DATA_3), content_type="application/json", headers=self.auth)
        self.assertEqual(response.status_code, 204)

    def test_5_graph_daterange(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(DATERANGE), content_type="application/json", headers=self.auth)
        self.assertEqual(response.status_code, 204)

    def test_6_graph_zonal_statistics(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(ZONAL_STATISTICS), content_type="application/json", headers=self.auth)
        self.assertEqual(response.status_code, 204)

    def test_9_graph_raster_export(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(RASTER_EXPORT), content_type="application/json", headers=self.auth)
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
