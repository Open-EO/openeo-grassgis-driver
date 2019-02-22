# -*- coding: utf-8 -*-
import unittest
from flask import json
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.udf import SUPPORTED_UDF
from openeo_grass_gis_driver.udf_lang_udf_type import python_udfs

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class UdfTestCase(TestBase):

    def otest_udf(self):
        response = self.app.get('/udf', headers=self.auth)
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data, SUPPORTED_UDF)

    def otest_udf_lang(self):
        response = self.app.get('/udf/python/udf_reduce_time', headers=self.auth)
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data, python_udfs["python"]["udf_reduce_time"])


if __name__ == "__main__":
    unittest.main()
