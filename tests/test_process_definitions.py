# -*- coding: utf-8 -*-
import unittest
from pprint import pprint
from openeo_grass_gis_driver.actinia_processing import config
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.actinia_processing.base import analyse_process_graph
from openeo_grass_gis_driver.utils.process_graph_examples_v03 import *

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessDefinitionTestCase(TestBase):

    def test_get_data_1(self):

        output_names, pc = analyse_process_graph(graph=GET_DATA_1)
        pprint(output_names)
        pprint(pc)

        self.assertEqual(len(pc), 1)

    def test_get_data_2(self):

        output_names, pc = analyse_process_graph(graph=GET_DATA_2)
        pprint(output_names)
        pprint(pc)

        self.assertEqual(len(pc), 2)

    def test_get_data_3(self):

        output_names, pc = analyse_process_graph(graph=GET_DATA_3)
        pprint(output_names)
        pprint(pc)

        self.assertEqual(len(pc), 1)

    def test_filter_bbox(self):

        output_names, pc = analyse_process_graph(graph=FILTER_BOX)
        pprint(output_names)
        pprint(pc)

        self.assertEqual(len(pc), 2)
        self.assertTrue(pc[1]["module"] == "g.region")

    def test_daterange(self):

        output_names, pc = analyse_process_graph(graph=DATERANGE)
        pprint(output_names)
        pprint(pc)

        self.assertEqual(len(pc), 2)

        self.assertTrue(pc[1]["module"] == "t.rast.extract")

    def test_reduce_time_min(self):

        name, pc = analyse_process_graph(graph=REDUCE_TIME_MIN)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 2)

    def test_ndvi_1(self):

        names, pc = analyse_process_graph(graph=NDVI_1)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[0], "lsat5_red_NDVI")
        self.assertEqual(len(pc), 4)

    def test_ndvi_2(self):

        names, pc = analyse_process_graph(graph=NDVI_2)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[0], "S2A_B04_NDVI")
        self.assertEqual(len(pc), 4)

    def test_ndvi_3(self):

        names, pc = analyse_process_graph(graph=NDVI_3)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[0], "lsat5_red_NDVI2")
        self.assertEqual(len(pc), 4)

    def test_ndvi_4(self):

        names, pc = analyse_process_graph(graph=NDVI_4)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[0], "S2A_B04_NDVI2")
        self.assertEqual(len(pc), 4)

    def test_raster_export(self):

        names, pc = analyse_process_graph(graph=RASTER_EXPORT)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[0], "nc_spm_08.PERMANENT.raster.elevation")
        self.assertEqual(names[1], "nc_spm_08.PERMANENT.raster.slope")
        self.assertEqual(len(pc), 4)

    def test_zonal_statistics(self):

        names, pc = analyse_process_graph(graph=ZONAL_STATISTICS)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[1], "latlong_wgs84.asia_gdd_2017.strds.gdd")
        self.assertEqual(names[0], "latlong_wgs84.modis_ndvi_global.strds.ndvi_16_5600m")
        self.assertEqual(len(pc), 16)

    def test_ndvi_error(self):

        try:
            names, pc = analyse_process_graph(graph=NDVI_ERROR)
            pprint(names)
            pprint(pc)
            self.assertTrue(False)
        except:
            pass

    def test_openeo_usecase_1(self):

        name, pc = analyse_process_graph(graph=OPENEO_USECASE_1)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 9)

    def test_openeo_usecase_1a(self):

        name, pc = analyse_process_graph(graph=OPENEO_USECASE_1A)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 8)

    def otest_openeo_usecase_2(self):
        # Disabled since UDF is not supported

        name, pc = analyse_process_graph(graph=OPENEO_USECASE_2)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 6)


if __name__ == "__main__":
    unittest.main()
