# -*- coding: utf-8 -*-
from flask import json
import unittest
from graas_openeo_core_wrapper.capabilities import GRAAS_CAPABILITIES
from graas_openeo_core_wrapper.test_base import TestBase

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class CapabilitiesTestCase(TestBase):

    def test_capabilities(self):
        response = self.app.get('/capabilities')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         GRAAS_CAPABILITIES)


if __name__ == "__main__":
    unittest.main()
