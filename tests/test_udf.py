# -*- coding: utf-8 -*-
import unittest
from flask import json
from graas_openeo_core_wrapper.test_base import TestBase
from graas_openeo_core_wrapper.udf import SUPPORTED_UDF
from graas_openeo_core_wrapper.udf_lang_udf_type import python_udfs

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class UdfTestCase(TestBase):

    def test_udf(self):
        response = self.app.get('/udf')
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data, SUPPORTED_UDF)

    def test_udf_lang(self):
        response = self.app.get('/udf/python/udf_reduce_time')
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data, python_udfs["python"]["udf_reduce_time"])


if __name__ == "__main__":
    unittest.main()
