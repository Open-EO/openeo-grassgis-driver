# -*- coding: utf-8 -*-
import unittest
from pprint import pprint
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.actinia_processing.base import Graph
from openeo_grass_gis_driver.utils.process_graph_examples_v10 import \
    GET_DATA_1, GET_DATA_2, GET_DATA_3, FILTER_BBOX, DATERANGE, \
    REDUCE_TIME_MIN, NDVI_STRDS, USE_CASE_1

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessDefinitionTestCase(TestBase):

    def test_get_data_1(self):

        g = Graph(GET_DATA_1)
        output_names, pc = g.to_actinia_process_list()
        pprint([str(o) for o in output_names])
        pprint(pc)
        self.assertEqual(len(pc), 2)

    def test_get_data_2(self):

        g = Graph(GET_DATA_2)
        output_names, pc = g.to_actinia_process_list()
        pprint([str(o) for o in output_names])
        pprint(pc)
        self.assertEqual(len(pc), 4)

    def test_get_data_3(self):

        g = Graph(GET_DATA_3)
        output_names, pc = g.to_actinia_process_list()
        pprint([str(o) for o in output_names])
        pprint(pc)
        self.assertEqual(len(pc), 3)
        self.assertTrue(pc[0]["module"] == "t.info")
        self.assertTrue(pc[1]["module"] == "g.region.bbox")
        self.assertTrue(pc[2]["module"] == "t.rast.extract")

    def test_filter_bbox(self):

        g = Graph(FILTER_BBOX)
        output_names, pc = g.to_actinia_process_list()
        pprint([str(o) for o in output_names])
        pprint(pc)
        self.assertEqual(len(pc), 3)
        self.assertTrue(pc[0]["module"] == "r.info")
        self.assertTrue(pc[1]["module"] == "g.region.bbox")
        self.assertTrue(pc[2]["module"] == "g.region.bbox")

#    def test_bbox_from_raster(self):
#
#        g = Graph(BBOX_FROM_RASTER)
#        output_names, pc = g.to_actinia_process_list()
#        pprint([str(o) for o in output_names])
#        pprint(pc)
#        self.assertEqual(len(pc), 3)
#        self.assertTrue(pc[0]["module"] == "r.info")
#        self.assertTrue(pc[1]["module"] == "g.region.bbox")
#        self.assertTrue(pc[2]["module"] == "g.region")

    def test_daterange(self):

        g = Graph(DATERANGE)
        output_names, pc = g.to_actinia_process_list()
        pprint([str(o) for o in output_names])
        pprint(pc)
        self.assertEqual(len(pc), 4)
        self.assertTrue(pc[0]["module"] == "t.info")
        self.assertTrue(pc[1]["module"] == "g.region.bbox")
        self.assertTrue(pc[2]["module"] == "t.rast.extract")
        self.assertTrue(pc[3]["module"] == "t.rast.extract")

#    def test_map_algebra(self):
#
#        g = Graph(MAP_ALGEBRA)
#        output_names, pc = g.to_actinia_process_list()
#        pprint([str(o) for o in output_names])
#        pprint(pc)
#        self.assertEqual(len(pc), 5)
#        self.assertTrue(pc[0]["module"] == "r.info")
#        self.assertTrue(pc[1]["module"] == "g.region.bbox")
#        self.assertTrue(pc[2]["module"] == "r.info")
#        self.assertTrue(pc[3]["module"] == "g.region.bbox")
#        self.assertTrue(pc[4]["module"] == "r.mapcalc")
#
#    def test_temporal_algebra(self):
#
#        g = Graph(TEMPORAL_ALGEBRA)
#        output_names, pc = g.to_actinia_process_list()
#        pprint([str(o) for o in output_names])
#        pprint(pc)
#        self.assertEqual(len(pc), 7)
#        self.assertTrue(pc[0]["module"] == "t.info")
#        self.assertTrue(pc[1]["module"] == "g.region.bbox")
#        self.assertTrue(pc[2]["module"] == "t.rast.extract")
#        self.assertTrue(pc[3]["module"] == "t.info")
#        self.assertTrue(pc[4]["module"] == "g.region.bbox")
#        self.assertTrue(pc[5]["module"] == "t.rast.extract")
#        self.assertTrue(pc[6]["module"] == "t.rast.algebra")

    def test_reduce_time_min(self):

        g = Graph(REDUCE_TIME_MIN)
        output_names, pc = g.to_actinia_process_list()
        pprint(output_names)
        pprint(pc)
        self.assertEqual(len(pc), 4)
        self.assertTrue(pc[0]["module"] == "t.info")
        self.assertTrue(pc[1]["module"] == "g.region.bbox")
        self.assertTrue(pc[2]["module"] == "t.rast.extract")
        self.assertTrue(pc[3]["module"] == "t.rast.series")

    def test_ndvi_1(self):

        g = Graph(NDVI_STRDS)
        output_names, pc = g.to_actinia_process_list()
        pprint([str(o) for o in output_names])
        pprint(pc)
        self.assertEqual(len(pc), 5)
        self.assertTrue(pc[0]["module"] == "t.info")
        self.assertTrue(pc[1]["module"] == "g.region.bbox")
        self.assertTrue(pc[2]["module"] == "t.rast.extract")
        self.assertTrue(pc[3]["module"] == "t.rast.ndvi")
        self.assertTrue(pc[4]["module"] == "t.rast.colors")
        self.assertTrue(
            "lsat5_1987_load_collection_ndvi" in [
                o.name for o in output_names])

#    def test_raster_export(self):
#
#        g = Graph(RASTER_EXPORT)
#        output_names, pc = g.to_actinia_process_list()
#        pprint([str(o) for o in output_names])
#        pprint(pc)
#        self.assertTrue(
#            "nc_spm_08.PERMANENT.raster.elevation"
#             in [o.full_name() for o in output_names])
#        self.assertEqual(len(pc), 3)
#
#    def test_rgb_raster_export(self):
#
#        g = Graph(RGB_RASTER_EXPORT)
#        output_names, pc = g.to_actinia_process_list()
#        pprint([str(o) for o in output_names])
#        pprint(pc)
#        self.assertTrue(
#            "nc_spm_08.landsat.raster.lsat7_2000_10"
#            in [o.full_name() for o in output_names])
#        self.assertTrue(
#            "nc_spm_08.landsat.raster.lsat7_2000_20"
#             in [o.full_name() for o in output_names])
#        self.assertTrue(
#            "nc_spm_08.landsat.raster.lsat7_2000_30"
#             in [o.full_name() for o in output_names])
#        self.assertEqual(len(pc), 8)
#
#    def test_zonal_statistics(self):
#
#        g = Graph(ZONAL_STATISTICS)
#        output_names, pc = g.to_actinia_process_list()
#        pprint([str(o) for o in output_names])
#        pprint(pc)
#        self.assertTrue(
#            'None.None.strds.LST_Day_monthly_load_collection'
#             in [o.full_name() for o in output_names])
#        self.assertEqual(len(pc), 10)

    def test_openeo_usecase_1(self):

        g = Graph(USE_CASE_1)
        output_names, pc = g.to_actinia_process_list()
        pprint([str(o) for o in output_names])
        pprint(pc)
        self.assertEqual(len(pc), 8)


if __name__ == "__main__":
    unittest.main()
