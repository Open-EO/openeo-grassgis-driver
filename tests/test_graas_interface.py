# -*- coding: utf-8 -*-
import unittest
from graas_openeo_core_wrapper.graas_wrapper import GRaaSInterface
from graas_openeo_core_wrapper.test_base import TestBase

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GRaaSInterfaceTestCase(TestBase):

    def test_health_check(self):

        iface = GRaaSInterface(self.gconf)
        self.assertTrue(iface.check_health())

    def test_list_raster(self):

        iface = GRaaSInterface(self.gconf)
        raster = iface.list_raster()
        print(raster)

    def test_list_vector(self):

        iface = GRaaSInterface(self.gconf)
        raster = iface.list_vector()
        print(raster)

    def test_list_strds(self):

        iface = GRaaSInterface(self.gconf)
        raster = iface.list_strds()
        print(raster)


if __name__ == "__main__":
    unittest.main()
