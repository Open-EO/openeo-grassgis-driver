# -*- coding: utf-8 -*-
import unittest
from pprint import pprint
from openeo_grass_gis_driver.actinia_processing import config
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.actinia_processing.base import process_node_to_actinia_process_chain, Node, Graph
from openeo_grass_gis_driver.utils.process_graph_examples_v04 import *

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessDefinitionTestCase(TestBase):

    def test_get_data_1(self):

        g = Graph(GET_DATA_1)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertEqual(len(pc), 1)

    def test_get_data_2(self):

        g = Graph(GET_DATA_2)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertEqual(len(pc), 2)

    def test_get_data_3(self):

        g = Graph(GET_DATA_3)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertTrue(pc[0]["module"] == "t.info")
        self.assertEqual(len(pc), 1)

    def test_filter_bbox(self):

        g = Graph(FILTER_BBOX)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertEqual(len(pc), 2)
        self.assertTrue(pc[0]["module"] == "r.info")
        self.assertTrue(pc[1]["module"] == "g.region")

    def test_daterange(self):

        g = Graph(DATERANGE)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertEqual(len(pc), 2)
        self.assertTrue(pc[0]["module"] == "t.info")
        self.assertTrue(pc[1]["module"] == "t.rast.extract")

    def test_map_algebra(self):

        g = Graph(MAP_ALGEBRA)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertEqual(len(pc), 3)
        self.assertTrue(pc[0]["module"] == "r.info")
        self.assertTrue(pc[1]["module"] == "r.info")
        self.assertTrue(pc[2]["module"] == "r.mapcalc")

    def test_temporal_algebra(self):

        g = Graph(TEMPORAL_ALGEBRA)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertEqual(len(pc), 3)
        self.assertTrue(pc[0]["module"] == "t.info")
        self.assertTrue(pc[1]["module"] == "t.info")
        self.assertTrue(pc[2]["module"] == "t.rast.algebra")

    def test_reduce_time_min(self):

        g = Graph(REDUCE_TIME_MIN)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertEqual(len(pc), 2)
        self.assertTrue(pc[0]["module"] == "t.info")
        self.assertTrue(pc[1]["module"] == "t.rast.series")

    def test_ndvi_1(self):

        g = Graph(NDVI_STRDS)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertEqual(len(pc), 4)
        self.assertTrue(pc[0]["module"] == "t.info")
        self.assertTrue(pc[1]["module"] == "t.info")
        self.assertTrue(pc[2]["module"] == "t.rast.mapcalc")
        self.assertTrue(pc[3]["module"] == "t.rast.colors")
        self.assertTrue("lsat5_red_NDVI" in output_names)

    def test_raster_export(self):

        g = Graph(RASTER_EXPORT)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertTrue("nc_spm_08.PERMANENT.raster.elevation" in output_names)
        self.assertEqual(len(pc), 2)

    def test_zonal_statistics(self):

        g = Graph(ZONAL_STATISTICS)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertTrue("latlong_wgs84.modis_ndvi_global.strds.ndvi_16_5600m" in output_names)
        self.assertEqual(len(pc), 8)

    def test_openeo_usecase_1(self):

        g = Graph(USE_CASE_1)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertEqual(len(pc), 8)


if __name__ == "__main__":
    unittest.main()
