# -*- coding: utf-8 -*-
import unittest
from pprint import pprint
from flask import json
from openeo_grass_gis_driver.test_base import TestBase

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessesTestCase(TestBase):

    def test_processes(self):
        response = self.app.get('/processes', headers=self.auth)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        pprint(data)

        self.assertEqual(len("processes"), 9)

#    def test_process_zonal_statistics(self):
#        response = self.app.get('/processes/zonal_statistics',
#                                headers=self.auth)
#        self.assertEqual(response.status_code, 200)
#        data = json.loads(response.data.decode())
#        pprint(data)
#
    def test_process_filter_bbox(self):
        response = self.app.get('/processes/filter_bbox', headers=self.auth)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        pprint(data)

    def test_process_get_data(self):
        response = self.app.get(
            '/processes/load_collection',
            headers=self.auth)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        pprint(data)

    def test_process_NDVI(self):
        response = self.app.get('/processes/ndvi', headers=self.auth)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        pprint(data)


if __name__ == "__main__":
    unittest.main()
