# -*- coding: utf-8 -*-
import unittest
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from graas_openeo_core_wrapper.test_base import TestBase
from pprint import pprint
import time

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GRaaSInterfaceTestCase(TestBase):

    def test_health_check(self):
        iface = GRaaSInterface(self.gconf)
        self.assertTrue(iface.check_health())

    def test_list_raster(self):
        iface = GRaaSInterface(self.gconf)
        status, layers = iface.list_raster(location="ECAD", mapset="PERMANENT")
        pprint(layers)

        self.assertEqual(status, 200)
        self.assertEqual(len(layers), 126)

    def test_list_vector(self):
        iface = GRaaSInterface(self.gconf)
        status, layers = iface.list_vector(location="ECAD", mapset="PERMANENT")
        pprint(layers)

        self.assertEqual(status, 200)
        self.assertEqual(len(layers), 0)

    def test_list_strds(self):
        iface = GRaaSInterface(self.gconf)
        status, layers = iface.list_strds(location="ECAD", mapset="PERMANENT")
        pprint(layers)

        self.assertEqual(status, 200)
        self.assertEqual(len(layers), 2)

    def test_strds_info(self):
        iface = GRaaSInterface(self.gconf)
        status, info = iface.layer_info(layer_name="ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm")
        pprint(info)

        self.assertEqual(status, 200)
        self.assertTrue("temporal_type" in info)
        self.assertTrue("aggregation_type" in info)
        self.assertTrue("creation_time" in info)
        self.assertTrue("creator" in info)
        self.assertTrue("granularity" in info)
        self.assertTrue("modification_time" in info)
        self.assertTrue("number_of_maps" in info)

    def test_mapset_info(self):
        iface = GRaaSInterface(self.gconf)
        status, info = iface.mapset_info(location="ECAD", mapset="PERMANENT")
        pprint(info)

        self.assertEqual(status, 200)
        self.assertTrue("region" in info)
        self.assertTrue("projection" in info)

    def test_list_mapsets(self):
        iface = GRaaSInterface(self.gconf)
        status, mapsets = iface.list_mapsets(location="ECAD")
        pprint(mapsets)

        self.assertEqual(status, 200)

    def test_layer_exists_1(self):
        iface = GRaaSInterface(self.gconf)
        status = iface.check_layer_exists(layer_name="ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm")
        self.assertTrue(status)

    def test_layer_exists_2(self):
        iface = GRaaSInterface(self.gconf)
        status = iface.check_layer_exists(layer_name="ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm")
        self.assertTrue(status)

    def test_layer_exists_2_error(self):
        iface = GRaaSInterface(self.gconf)
        status = iface.check_layer_exists(layer_name="ECAD.PERMANENT.strds.precipitation_1950_2013_yearly_mm_nope")
        self.assertFalse(status)

    def test_layer_exists_4(self):
        iface = GRaaSInterface(self.gconf)
        status = iface.check_layer_exists(layer_name="ECAD.PERMANENT.raster.precipitation_yearly_mm_0")
        self.assertTrue(status)

    def test_async_persistent_processing(self):

        iface = GRaaSInterface(self.gconf)
        process_chain = {
            "version": "1",
            "list": [
                {"id": "g_region_1",
                 "module": "g.region",
                 "flags": "g"}]}

        status, resource_id = iface.async_persistent_processing(location="LL",
                                                                mapset="new_user_mapset",
                                                                process_chain=process_chain)
        print(status)
        print(resource_id)
        self.assertEqual(status, 200)

        status, info = iface.resource_info(resource_id)
        print(status)
        print(info)

        time.sleep(2)

        status, info = iface.resource_info(resource_id)
        print(status)
        print(info)

    def test_mapset_creation_deletion(self):

        config = self.gconf
        config.USER = "admin"
        iface = GRaaSInterface(config)
        status, resource_id = iface.create_mapset(location="LL", mapset="new_mapset")
        print(status)
        self.assertEqual(status, 200)
        print(resource_id)
        status, resource_id = iface.delete_mapset(location="LL", mapset="new_mapset")
        print(status)
        self.assertEqual(status, 200)
        print(resource_id)


if __name__ == "__main__":
    unittest.main()
