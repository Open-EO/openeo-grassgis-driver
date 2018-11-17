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
        response = self.app.get('/processes')
        data = json.loads(response.data.decode())
        pprint(data)

        self.assertEqual(len("processes"), 9)


if __name__ == "__main__":
    unittest.main()
