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

        self.assertEqual(len(data), 2)

        dsets = ["precipitation_1950_2013_yearly_mm",
                 "temperature_mean_1950_2013_yearly_celsius"]

        for entry in data:
            print(entry["product_id"])
            self.assertTrue(entry["product_id"] in dsets)


if __name__ == "__main__":
    unittest.main()
