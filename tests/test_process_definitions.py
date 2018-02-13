# -*- coding: utf-8 -*-
import unittest
from pprint import pprint
from graas_openeo_core_wrapper.test_base import TestBase
from graas_openeo_core_wrapper.process_definitions import analyse_process_graph

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessDefinitionTestCase(TestBase):

    def test_min_time(self):
        graph = {
            "process_graph": {
                "process_id": "min_time",
                "args": {
                    "collections": [{
                        "process_id": "min_time",
                        "args": {
                            "collections": [{
                                "process_id": "min_time",
                                "args": {
                                    "collections": [{
                                        "process_id": "min_time",
                                        "args": {
                                            "collections": [{"product_id": "time_series"}]
                                        }
                                    }],
                                }
                            }],
                        }
                    }]
                }
            }
        }

        name, pc = analyse_process_graph(graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 4)

        for entry in pc:
            self.assertTrue(entry["module"] == "t.rast.series")

    def test_filter_bbox(self):
        graph = {
            "process_graph": {
                "process_id": "filter_bbox",
                "args": {
                    "collections": [{"product_id": "temperature_mean_1950_2013_yearly_celsius@PERMANENT"}],
                    "left": -40.5,
                    "right": 75.5,
                    "top": 75.5,
                    "bottom": 25.25
                }
            }
        }

        name, pc = analyse_process_graph(graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 1)

        for entry in pc:
            self.assertTrue(entry["module"] == "g.region")

    def test_daterange(self):
        graph = {
            "process_graph": {
                "process_id": "filter_daterange",
                "args": {
                    "collections": [{"product_id": "temperature_mean_1950_2013_yearly_celsius@PERMANENT"}],
                    "from": "2001-01-01",
                    "to": "2005-01-01"
                }
            }
        }

        name, pc = analyse_process_graph(graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 1)

        for entry in pc:
            self.assertTrue(entry["module"] == "t.rast.extract")

    def test_ndvi(self):
        graph = {
            "process_graph": {
                "process_id": "NDVI",
                "args": {
                    "collections": [{"product_id": "temperature_mean_1950_2013_yearly_celsius@PERMANENT"}],
                    "nir": "temperature_mean_1950_2013_yearly_celsius@PERMANENT",
                    "red": "temperature_mean_1950_2013_yearly_celsius@PERMANENT"
                }
            }
        }

        name, pc = analyse_process_graph(graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 2)

    def test_openeo_usecase_1(self):

        graph = {
            "process_graph": {
                "process_id": "min_time",
                "args": {
                    "collections": [{
                        "process_id": "NDVI",
                        "args": {
                            "collections": [{
                                "process_id": "filter_daterange",
                                "args": {
                                    "collections": [{
                                        "process_id": "filter_bbox",
                                        "args": {
                                            "collections": [{
                                                "product_id": "temperature_mean_1950_2013_yearly_celsius@PERMANENT"
                                            }],
                                            "left": 652000,
                                            "right": 672000,
                                            "top": 5161000,
                                            "bottom": 5181000,
                                            "srs": "EPSG:32632"
                                        }
                                    }],
                                    "from": "2017-01-01",
                                    "to": "2017-01-31"
                                }
                            }],
                            "red": "B04",
                            "nir": "B8A"
                        }
                    }]
                }
            }
        }

        name, pc = analyse_process_graph(graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 1)


if __name__ == "__main__":
    unittest.main()
