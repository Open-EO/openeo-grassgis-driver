# -*- coding: utf-8 -*-
import unittest
from openeo_grass_gis_driver.actinia_processing.actinia_interface import \
     ActiniaInterface
from openeo_grass_gis_driver.test_base import TestBase
from pprint import pprint
import time

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ActiniaInterfaceTestCase(TestBase):

    def test_health_check(self):
        iface = ActiniaInterface(self.gconf)
        self.assertTrue(iface.check_health())

    def test_list_raster(self):
        iface = ActiniaInterface(self.gconf)
        status, layers = iface.list_raster(
            location="nc_spm_08", mapset="PERMANENT")
        pprint(layers)

        self.assertEqual(status, 200)
        self.assertEqual(len(layers), 41)

    def test_list_vector(self):
        iface = ActiniaInterface(self.gconf)
        status, layers = iface.list_vector(
            location="nc_spm_08", mapset="PERMANENT")
        pprint(layers)

        self.assertEqual(status, 200)
        self.assertEqual(len(layers), 46)

    def test_list_strds(self):
        iface = ActiniaInterface(self.gconf)
        status, layers = iface.list_strds(
            location="nc_spm_08", mapset="landsat")
        pprint(layers)

        self.assertEqual(status, 200)
        self.assertEqual(len(layers), 1)

    def test_strds_info(self):
        iface = ActiniaInterface(self.gconf)
        status, info = iface.layer_info(
            layer_name="nc_spm_08.landsat.strds.lsat5_1987")
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
        iface = ActiniaInterface(self.gconf)
        status, info = iface.mapset_info(
            location="nc_spm_08", mapset="PERMANENT")
        pprint(info)

        self.assertEqual(status, 200)
        self.assertTrue("region" in info)
        self.assertTrue("projection" in info)

    def test_list_mapsets(self):
        iface = ActiniaInterface(self.gconf)
        status, mapsets = iface.list_mapsets(location="nc_spm_08")
        pprint(mapsets)

        self.assertEqual(status, 200)

    def test_layer_exists_1(self):
        iface = ActiniaInterface(self.gconf)
        status = iface.check_layer_exists(
            layer_name="nc_spm_08.landsat.raster.lsat5_1987_10")
        self.assertTrue(status)

    def test_layer_exists_2(self):
        iface = ActiniaInterface(self.gconf)
        status = iface.check_layer_exists(
            layer_name="nc_spm_08.landsat.strds.lsat5_1987")
        self.assertTrue(status)

    def test_layer_exists_2_error(self):
        iface = ActiniaInterface(self.gconf)
        layer_name = "nc_spm_08.landsat.strds.lsat5_1987_nope"
        status = iface.check_layer_exists(
            layer_name=layer_name)
        self.assertFalse(status)

    def test_async_persistent_processing(self):

        iface = ActiniaInterface(self.gconf)
        process_chain = {
            "version": "1",
            "list": [
                {"id": "g_region_1",
                 "module": "g.region",
                 "flags": "g"}]}

        status, response = iface.async_persistent_processing(
            location="nc_spm_08", mapset="new_user_mapset",
            process_chain=process_chain)
        resource_id = response["resource_id"]
        print(status)
        print(resource_id)
        self.assertEqual(status, 200)

        status, info = iface.resource_info(resource_id)
        print(status)
        print(info)

        time.sleep(5)

        status, info = iface.resource_info(resource_id)
        print(status)
        print(info)
        self.assertEqual(info["status"], "finished")

    def disfunc_test_mapset_creation_deletion(self):

        config = self.gconf
        iface = ActiniaInterface(config)
        status, response = iface.create_mapset(
            location="nc_spm_08", mapset="new_mapset")
        print(status)
        self.assertEqual(status, 200)
        print(response)
        status, response = iface.delete_mapset(
            location="nc_spm_08", mapset="new_mapset")
        print(status)
        self.assertEqual(status, 200)
        print(response)


if __name__ == "__main__":
    unittest.main()
