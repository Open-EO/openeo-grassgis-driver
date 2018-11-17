# -*- coding: utf-8 -*-
import unittest
from pprint import pprint
from openeo_grass_gis_driver.actinia_processing import config
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.actinia_processing.base import analyse_process_graph

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessDefinitionTestCase(TestBase):

    def test_get_data_1(self):
        graph = {
            "process_graph": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.PERMANENT.raster.elevation"
            }
        }

        output_names, pc = analyse_process_graph(graph=graph)
        pprint(output_names)
        pprint(pc)

        self.assertEqual(len(pc), 1)

    def test_get_data_2(self):
        graph = {
            "process_graph": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.PERMANENT.raster.elevation",
                "imagery": {
                    "process_id": "get_data",
                    "data_id": "nc_spm_08.PERMANENT.vector.lakes",
                    "imagery": {
                        "process_id": "get_data",
                        "data_id": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"
                    }
                }
            }
        }

        output_names, pc = analyse_process_graph(graph=graph)
        pprint(output_names)
        pprint(pc)

        self.assertEqual(len(pc), 3)

    def test_filter_bbox(self):
        graph = {
            "process_graph": {
                "process_id": "filter_bbox",
                "imagery": {
                    "process_id": "get_data",
                    "data_id": "nc_spm_08.PERMANENT.raster.elevation"
                },
                "spatial_extent": {
                    "left": -40.5,
                    "right": 75.5,
                    "top": 75.5,
                    "bottom": 25.25,
                    "width_res": 0.1,
                    "height_res": 0.1,
                }
            }
        }

        output_names, pc = analyse_process_graph(graph=graph)
        pprint(output_names)
        pprint(pc)

        self.assertEqual(len(pc), 2)
        self.assertTrue(pc[1]["module"] == "g.region")

    def test_daterange(self):
        graph = {
            "process_graph": {
                "process_id": "filter_daterange",
                "from": "2001-01-01",
                "to": "2005-01-01",
                "strds_data": {
                    "process_id": "get_data",
                    "data_id": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"
                }

            }
        }

        output_names, pc = analyse_process_graph(graph=graph)
        pprint(output_names)
        pprint(pc)

        self.assertEqual(len(pc), 2)

        self.assertTrue(pc[1]["module"] == "t.rast.extract")

    def test_reduce_time_min(self):

        graph = {
            "process_graph": {
                "process_id": "reduce_time",
                "method": "minimum",
                "images": {
                    "process_id": "get_data",
                    "data_id": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"
                }

            }
        }
        name, pc = analyse_process_graph(graph=graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 2)

    def test_ndvi(self):

        graph = {
            "process_graph": {
                "process_id": "NDVI",
                "red": {
                    "process_id": "get_data",
                    "data_id": "nc_spm_08.landsat.strds.lsat5_red"
                },
                "nir": {
                    "process_id": "get_data",
                    "data_id": "nc_spm_08.landsat.strds.lsat5_nir"
                }
            }
        }
        names, pc = analyse_process_graph(graph=graph)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[0], "lsat5_red_NDVI")
        self.assertEqual(len(pc), 4)

        graph = {
            "process_graph": {
                "process_id": "NDVI",
                "nir": {
                    "process_id": "get_data",
                    "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                },
                "red": {
                    "process_id": "get_data",
                    "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                }
            }
        }
        names, pc = analyse_process_graph(graph=graph)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[0], "S2A_B04_NDVI")
        self.assertEqual(len(pc), 4)

    def test_raster_export(self):

        graph = {
            "process_graph": {
                "process_id": "raster_exporter",
                "imagery": {
                    "process_id": "get_data",
                    "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08",
                    "imagery": {
                        "process_id": "get_data",
                        "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                    }
                }
            }
        }
        names, pc = analyse_process_graph(graph=graph)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[0], "LL.sentinel2A_openeo_subset.strds.S2A_B08")
        self.assertEqual(names[1], "LL.sentinel2A_openeo_subset.strds.S2A_B04")
        self.assertEqual(len(pc), 4)

    def test_zonal_statistics(self):

        graph = {
            "process_graph": {
                "process_id": "zonal_statistics",
                "imagery": {
                    "process_id": "get_data",
                    "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08",
                    "imagery": {
                        "process_id": "get_data",
                        "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                    }
                },
                "polygons": "https://storage.googleapis.com/graas-geodata/roi_openeo_use_case_2.geojson"
            }
        }
        names, pc = analyse_process_graph(graph=graph)
        pprint(names)
        pprint(pc)

        self.assertEqual(names[0], "LL.sentinel2A_openeo_subset.strds.S2A_B08")
        self.assertEqual(names[1], "LL.sentinel2A_openeo_subset.strds.S2A_B04")
        self.assertEqual(len(pc), 16)

    def test_ndvi_error(self):
        graph = {
            "process_graph": {
                "process_id": "NDVI_nope",
                "nir": {
                    "process_id": "get_data",
                    "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                },
                "red": {
                    "process_id": "get_data",
                    "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                }
            }
        }

        try:
            names, pc = analyse_process_graph(graph=graph)
            pprint(names)
            pprint(pc)
            self.assertTrue(False)
        except:
            pass

    def otest_openeo_usecase_1(self):

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
                                                    "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
                                                }],
                                                "left": -5.0,
                                                "right": -4.7,
                                                "top": 39.3,
                                                "bottom": 39.0,
                                                "ewres": 0.1,
                                                "nsres": 0.1,
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
                                                        "product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                                                    }],
                                                    "left": -5.0,
                                                    "right": -4.7,
                                                    "top": 39.3,
                                                    "bottom": 39.0,
                                                    "ewres": 0.1,
                                                    "nsres": 0.1,
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

        name, pc = analyse_process_graph(graph=graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 7)

    def otest_openeo_usecase_1a(self):

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
                                                "collections": [
                                                    {"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"},
                                                    {"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"}],
                                                "left": -5.0,
                                                "right": -4.7,
                                                "top": 39.3,
                                                "bottom": 39.0,
                                                "ewres": 0.1,
                                                "nsres": 0.1,
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

        name, pc = analyse_process_graph(graph=graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 7)

    def otest_openeo_usecase_2(self):

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
                                        "collections": [{"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"},
                                                        {"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"}],
                                        "left": -5.0,
                                        "right": -4.7,
                                        "top": 39.3,
                                        "bottom": 39.0,
                                        "ewres": 0.1,
                                        "nsres": 0.1,
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

        name, pc = analyse_process_graph(graph=graph)
        pprint(name)
        pprint(pc)

        self.assertEqual(len(pc), 6)


if __name__ == "__main__":
    unittest.main()
