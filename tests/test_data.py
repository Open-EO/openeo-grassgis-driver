# -*- coding: utf-8 -*-
import unittest
from flask import json
from graas_openeo_core_wrapper.test_base import TestBase

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DataTestCase(TestBase):

    def test_data(self):
        response = self.app.get('/data')
        data = json.loads(response.data.decode())
        print(data)

        self.assertTrue(len(data), 2)

        dsets = ["ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm",
                 "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"]

        for entry in data:
            print(entry["product_id"])
            if "ECAD.PERMANENT.strds" in entry["product_id"]:
                self.assertTrue(entry["product_id"] in dsets)

    def test_strds_product_id_1(self):
        response = self.app.get('/data/ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data["product_id"], "ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm")

    def test_strds_product_id_2(self):
        response = self.app.get('/data/ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data["product_id"], "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius")

    def test_raster_product_id_1(self):
        response = self.app.get('/data/ECAD.PERMANENT.raster.precipitation_yearly_mm_0')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data["product_id"], "ECAD.PERMANENT.raster.precipitation_yearly_mm_0")

    def test_raster_product_id_2(self):
        response = self.app.get('/data/ECAD.PERMANENT.raster.temperature_mean_yearly_celsius_0')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data["product_id"], "ECAD.PERMANENT.raster.temperature_mean_yearly_celsius_0")


if __name__ == "__main__":
    unittest.main()
