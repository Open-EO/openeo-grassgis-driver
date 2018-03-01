# -*- coding: utf-8 -*-
import unittest
from flask import json
from graas_openeo_core_wrapper.test_base import TestBase
from graas_openeo_core_wrapper.udf import SUPPORTED_UDF

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class UdfTestCase(TestBase):

    def test_1(self):
        response = self.app.get('/udf')
        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(data, SUPPORTED_UDF)


if __name__ == "__main__":
    unittest.main()
