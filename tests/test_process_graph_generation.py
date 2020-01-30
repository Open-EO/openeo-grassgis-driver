# -*- coding: utf-8 -*-
import unittest
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.actinia_processing.base import Node, Graph
from openeo_grass_gis_driver.utils.process_graph_examples_v04 import OPENEO_EXAMPLE_1, \
  FILTER_BBOX, NDVI_STRDS, USE_CASE_1, ZONAL_STATISTICS, DATERANGE

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GraphValidationTestCase(TestBase):

    def test_graph_creation_openeo_example(self):

        pg = Graph(OPENEO_EXAMPLE_1)
        self.assertEqual(2, len(pg.root_nodes))
        self.assertEqual(9, len(pg.node_dict))

        print(pg.node_dict["export1"])
        print(pg.node_dict["export2"])
        print(pg.node_dict["filter1"])
        print(pg.node_dict["filter2"])
        print(pg.node_dict["filter3"])
        print(pg.node_dict["getcol1"])
        print(pg.node_dict["mergec1"])
        print(pg.node_dict["reduce1"])
        print(pg.node_dict["reduce2"])

    def test_graph_creation_graph_filter_bbox(self):

        pg = Graph(FILTER_BBOX)

        print(pg.node_dict["get_data_1"])
        print(pg.node_dict["filter_bbox_1"])

        self.assertEqual(1, len(pg.root_nodes))
        self.assertEqual(2, len(pg.node_dict))

        self.assertIsNone(pg.node_dict["filter_bbox_1"].child)
        self.assertEqual(pg.node_dict["filter_bbox_1"], pg.node_dict["get_data_1"].child)
        self.assertEqual(pg.node_dict["filter_bbox_1"].get_parent_by_name("data"), pg.node_dict["get_data_1"])
        self.assertEqual(1, len(pg.node_dict["filter_bbox_1"].parents))
        self.assertTrue(pg.node_dict["get_data_1"] in pg.node_dict["filter_bbox_1"].parents)

    def test_graph_creation_graph_zonal_statistics(self):

        pg = Graph(ZONAL_STATISTICS)

        print(pg.node_dict["zonal_statistics_1"])
        print(pg.node_dict["get_b08_data"])

        self.assertEqual(1, len(pg.root_nodes))
        self.assertEqual(2, len(pg.node_dict))

        self.assertIsNone(pg.node_dict["zonal_statistics_1"].child)
        self.assertEqual(pg.node_dict["zonal_statistics_1"], pg.node_dict["get_b08_data"].child)
        self.assertEqual(pg.node_dict["zonal_statistics_1"].get_parent_by_name("data"), pg.node_dict["get_b08_data"])
        self.assertEqual(1, len(pg.node_dict["zonal_statistics_1"].parents))
        self.assertTrue(pg.node_dict["get_b08_data"] in pg.node_dict["zonal_statistics_1"].parents)

    def test_graph_creation_graph_daterange(self):

        pg = Graph(DATERANGE)

        print(pg.node_dict["filter_daterange_1"])
        print(pg.node_dict["get_strds_data"])

        self.assertEqual(1, len(pg.root_nodes))
        self.assertEqual(2, len(pg.node_dict))

        self.assertIsNone(pg.node_dict["filter_daterange_1"].child)
        self.assertEqual(pg.node_dict["filter_daterange_1"], pg.node_dict["get_strds_data"].child)
        self.assertEqual(pg.node_dict["filter_daterange_1"].get_parent_by_name("data"), pg.node_dict["get_strds_data"])
        self.assertEqual(1, len(pg.node_dict["filter_daterange_1"].parents))
        self.assertTrue(pg.node_dict["get_strds_data"] in pg.node_dict["filter_daterange_1"].parents)

    def test_graph_creation_graph_ndvi_strds(self):

        pg = Graph(NDVI_STRDS)

        print(pg.node_dict["get_data"])
        print(pg.node_dict["ndvi_1"])

        self.assertEqual(1, len(pg.root_nodes))
        self.assertEqual(2, len(pg.node_dict))

        self.assertIsNone(pg.node_dict["ndvi_1"].child)
        self.assertEqual(1, len(pg.node_dict["ndvi_1"].parents))
        self.assertTrue(pg.node_dict["get_data"] in pg.node_dict["ndvi_1"].parents)

        self.assertEqual(pg.node_dict["ndvi_1"], pg.node_dict["get_data"].child)

        self.assertEqual(pg.node_dict["ndvi_1"].parents_dict["data"], pg.node_dict["get_data"])

    def test_graph_creation_graph_use_case_1(self):

        pg = Graph(USE_CASE_1)

        print(pg.node_dict["get_data"])
        print(pg.node_dict["filter_bbox"])
        print(pg.node_dict["ndvi_1"])
        print(pg.node_dict["filter_daterange_ndvi"])
        print(pg.node_dict["reduce_time_1"])

        self.assertEqual(1, len(pg.root_nodes))
        self.assertEqual(5, len(pg.node_dict))

if __name__ == "__main__":
    unittest.main()
