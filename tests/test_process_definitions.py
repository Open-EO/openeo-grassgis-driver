# -*- coding: utf-8 -*-
import unittest
from pprint import pprint
from graas_openeo_core_wrapper import config
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

        config.Config.LOCATION = "ECAD"
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

        config.Config.LOCATION = "ECAD"
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

        config.Config.LOCATION = "ECAD"
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
                    "collections": [{"product_id": "S2A_B04@sentinel2A_openeo_subset"},
                                    {"product_id": "S2A_B08@sentinel2A_openeo_subset"}],
                    "red": "S2A_B04",
                    "nir": "S2A_B08"
                }
            }
        }

        config.Config.LOCATION = "LL"

        names, pc = analyse_process_graph(graph)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[0], "S2A_B04_NDVI")
        self.assertEqual(len(pc), 2)

    def test_ndvi_error(self):
        graph = {
            "process_graph": {
                "process_id": "NDVI_nope",
                "args": {
                    "collections": [{"product_id": "S2A_B04@sentinel2A_openeo_subset"},
                                    {"product_id": "S2A_B08@sentinel2A_openeo_subset"}],
                    "red": "S2A_B04",
                    "nir": "S2A_B08"
                }
            }
        }

        config.Config.LOCATION = "LL"

        try:
            names, pc = analyse_process_graph(graph)
            pprint(names)
            pprint(pc)
            self.assertTrue(False)
        except:
            pass

    def test_openeo_usecase_1(self):

        graph = \
            {
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
                                                    "product_id": "S2A_B04@sentinel2A_openeo_subset"
                                                }],
                                                "left": -5.0,
                                                "right": -4.7,
                                                "top": 39.3,
                                                "bottom": 39.0,
                                                "srs": "EPSG:4326"
                                            }
                                        }],
                                        "from": "2017-04-12 11:17:08",
                                        "to": "2017-09-04 11:18:26"
                                    }
                                },
                                    {
                                        "process_id": "filter_daterange",
                                        "args": {
                                            "collections": [{
                                                "process_id": "filter_bbox",
                                                "args": {
                                                    "collections": [{
                                                        "product_id": "S2A_B08@sentinel2A_openeo_subset"
                                                    }],
                                                    "left": -5.0,
                                                    "right": -4.7,
                                                    "top": 39.3,
                                                    "bottom": 39.0,
                                                    "srs": "EPSG:4326"
                                                }
                                            }],
                                            "from": "2017-04-12 11:17:08",
                                            "to": "2017-09-04 11:18:26"
                                        }
                                    }],
                                "red": "S2A_B04",
                                "nir": "S2A_B08"
                            }
                        }]
                    }
                }
            }

        config.Config.LOCATION = "LL"

        name, pc = analyse_process_graph(graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 7)

    def test_openeo_usecase_1a(self):

        graph = \
            {
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
                                                "collections": [{"product_id": "S2A_B04@sentinel2A_openeo_subset"},
                                                                {"product_id": "S2A_B08@sentinel2A_openeo_subset"}],
                                                "left": -5.0,
                                                "right": -4.7,
                                                "top": 39.3,
                                                "bottom": 39.0,
                                                "srs": "EPSG:4326"
                                            }
                                        }],
                                        "from": "2017-04-12 11:17:08",
                                        "to": "2017-09-04 11:18:26"
                                    }
                                }],
                                "red": "S2A_B04",
                                "nir": "S2A_B08"
                            }
                        }]
                    }
                }
            }

        config.Config.LOCATION = "LL"

        name, pc = analyse_process_graph(graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 7)

    def test_openeo_usecase_2(self):

        graph = \
            {
                "process_graph": {
                    "process_id": "udf_reduce_time",
                    "args": {
                        "collections": [{
                            "process_id": "filter_daterange",
                            "args": {
                                "collections": [{
                                    "process_id": "filter_bbox",
                                    "args": {
                                        "collections": [
                                            {"product_id": "temperature_mean_1950_2013_yearly_celsius@PERMANENT"},
                                            {"product_id": "precipitation_1950_2013_yearly_mm@PERMANENT"}],
                                        "left": -5.0,
                                        "right": -4.7,
                                        "top": 39.3,
                                        "bottom": 39.0,
                                        "srs": "EPSG:4326"
                                    }
                                }],
                                "from": "1980-01-01 00:00:00",
                                "to": "2010-01-01 00:00:00"
                            }
                        }],
                        "python_file_url": "https://storage.googleapis.com/datentransfer/aggr_func.py"
                    }
                }
            }

        config.Config.LOCATION = "ECAD"

        name, pc = analyse_process_graph(graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 6)


if __name__ == "__main__":
    unittest.main()
