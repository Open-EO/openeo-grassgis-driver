# -*- coding: utf-8 -*-
import unittest
import time
import pprint
from flask import json
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.actinia_processing import config

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

graph_filter_bbox_nc = {
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

graph_ndvi_strds = {
    "process_graph": {
        "process_id": "NDVI",
        "red": "lsat5_red",
        "nir": "lsat5_nir",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.landsat.strds.lsat5_red",
            "imagery": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.landsat.strds.lsat5_nir"
            }
        }
    }
}

graph_use_case_1 = {
    "process_graph": {
        "process_id": "reduce_time",
        "method": "minimum",
        "imagery": {
            "process_id": "NDVI",
            "red": "lsat5_red",
            "nir": "lsat5_nir",
            "imagery": {
                "process_id": "filter_daterange",
                "from": "2001-01-01",
                "to": "2005-01-01",
                "imagery": {
                    "process_id": "filter_bbox",
                    "imagery": {
                        "process_id": "get_data",
                        "data_id": "nc_spm_08.landsat.strds.lsat5_red",
                        "imagery": {
                            "process_id": "get_data",
                            "data_id": "nc_spm_08.landsat.strds.lsat5_nir",
                        }
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

        }
    }
}


class GraphValidationTestCase(TestBase):

    def test_1_graph_filter_bbox_nc(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(graph_filter_bbox_nc), content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_2_graph_ndvi(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(graph_ndvi_strds), content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_3_use_case_1(self):
        """Run the validation test
        """
        response = self.app.post('/validation', data=json.dumps(graph_use_case_1), content_type="application/json")
        self.assertEqual(response.status_code, 204)


if __name__ == "__main__":
    unittest.main()
