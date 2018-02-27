# -*- coding: utf-8 -*-
import unittest
from flask import json
from graas_openeo_core_wrapper.test_base import TestBase
from graas_openeo_core_wrapper import config

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

use_case_1_graph = {
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
                                        "right": -4.98,
                                        "top": 39.12,
                                        "bottom": 39.1,
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

date_range_filter = {
    "process_graph": {
        "process_id": "filter_daterange",
        "args": {
            "collections": [{
                "process_id": "filter_bbox",
                "args": {
                    "collections": [{
                        "product_id": "S2A_B04@sentinel2A_openeo_subset"
                    }],
                    "left": -5.0,
                    "right": -4.98,
                    "top": 39.12,
                    "bottom": 39.1,
                    "srs": "EPSG:4326"
                }
            }],
            "from": "2017-06-21 11:12:22",
            "to": "2017-08-20 11:12:21"
        }
    }
}


class JobsTestCase(TestBase):

    def test_post_use_case_1_job(self):
        config.Config.LOCATION = "LL"
        response = self.app.post('/jobs', data=json.dumps(use_case_1_graph), content_type="application/json")

        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(response.status_code, 200)

    def test_post_data_range_filter_job(self):
        config.Config.LOCATION = "LL"
        response = self.app.post('/jobs', data=json.dumps(date_range_filter), content_type="application/json")

        data = json.loads(response.data.decode())
        print(data)

        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
