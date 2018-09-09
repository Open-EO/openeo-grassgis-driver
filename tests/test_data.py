# -*- coding: utf-8 -*-
import unittest
from flask import json
from pprint import pprint
from openeo_grass_gis_driver.test_base import TestBase

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DataTestCase(TestBase):

    def test_data(self):
        response = self.app.get('/data')
        data = json.loads(response.data.decode())

        self.assertTrue(len(data), 2)

        dsets = ["nc_spm_08.landsat.raster.lsat5_1987_10",
                 "nc_spm_08.PERMANENT.vector.lakes",
                 "nc_spm_08.PERMANENT.raster.elevation"]

        data_id_list = []

        for entry in data:
            data_id_list.append(entry["data_id"])

        found = False
        for entry in dsets:
            self.assertTrue(entry in data_id_list)
            found = True

        self.assertTrue(found)

    def test_raster_data_id_1(self):
        response = self.app.get('/data/nc_spm_08.landsat.raster.lsat5_1987_10')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        pprint(data)

        self.assertEqual(data["data_id"], "nc_spm_08.landsat.raster.lsat5_1987_10")

    def test_raster_data_id_2(self):
        response = self.app.get('/data/nc_spm_08.PERMANENT.raster.elevation')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        pprint(data)

        self.assertEqual(data["data_id"], "nc_spm_08.PERMANENT.raster.elevation")

    def test_vector_data_id_2(self):
        response = self.app.get('/data/nc_spm_08.PERMANENT.raster.elevation')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode())
        pprint(data)

        self.assertEqual(data["data_id"], "nc_spm_08.PERMANENT.raster.elevation")


if __name__ == "__main__":
    unittest.main()
