# -*- coding: utf-8 -*-
import unittest

from openeo_grass_gis_driver.test_base import TestBase

__license__ = "Apache License, Version 2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021, mundialis"
__maintainer__ = "mundialis"


class UdfTestCase(TestBase):

    def test_well_known(self):
        response = self.app.get('/.well-known/openeo', headers=self.auth)
        self.assertEqual(response.status_code, 200)

    def test_well_known_with_api_prefix(self):
        response = self.app.get(
            self.prefix + '/.well-known/openeo', headers=self.auth)
        self.assertEqual(response.status_code, 404)


if __name__ == "__main__":
    unittest.main()
