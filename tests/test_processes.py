# -*- coding: utf-8 -*-
import unittest
from flask import json
from graas_openeo_core_wrapper.test_base import TestBase

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessesTestCase(TestBase):

    def test_processes(self):
        response = self.app.get('/processes')
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(len(data), 5)

        dsets = ["filter_bbox",
                 "filter_daterange",
                 "min_time",
                 "NDVI",
                 "udf_reduce_time"]

        for entry in data:
            self.assertTrue(entry in dsets)

    def test_process_id_1(self):
        response = self.app.get('/processes/filter_bbox')
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data["process_id"], "filter_bbox")

    def test_process_id_2(self):
        response = self.app.get('/processes/filter_daterange')
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data["process_id"], "filter_daterange")

    def test_process_id_3(self):
        response = self.app.get('/processes/NDVI')
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data["process_id"], "NDVI")

    def test_process_id_4(self):
        response = self.app.get('/processes/min_time')
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data["process_id"], "min_time")

    def test_process_id_5(self):
        response = self.app.get('/processes/udf_reduce_time')
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data["process_id"], "udf_reduce_time")


if __name__ == "__main__":
    unittest.main()
