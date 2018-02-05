# -*- coding: utf-8 -*-
import unittest
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
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
        layer = iface.list_raster(mapset="PERMANENT")
        print(layer)

    def test_list_vector(self):

        iface = GRaaSInterface(self.gconf)
        layer = iface.list_vector(mapset="PERMANENT")
        print(layer)

    def test_list_strds(self):

        iface = GRaaSInterface(self.gconf)
        layer = iface.list_strds(mapset="PERMANENT")
        print(layer)

    def test_strds_info(self):

        iface = GRaaSInterface(self.gconf)
        info = iface.strds_info(mapset="PERMANENT",
                                strds_name="precipitation_1950_2013_yearly_mm")
        print(info)

    def test_mapset_info(self):

        iface = GRaaSInterface(self.gconf)
        info = iface.mapset_info(mapset="PERMANENT")
        print(info)

    def test_list_mapsets(self):

        iface = GRaaSInterface(self.gconf)
        layer = iface.list_mapsets()
        print(layer)


if __name__ == "__main__":
    unittest.main()
