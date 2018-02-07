# -*- coding: utf-8 -*-
from flask import json
import unittest
from graas_openeo_core_wrapper.capabilities import GRAAS_CAPABILITIES
from graas_openeo_core_wrapper.test_base import TestBase
import graas_openeo_core_wrapper.process_definitions.min_time_process as min_time

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class CapabilitiesTestCase(TestBase):

    def test_min_time(self):
        leaf = {
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
                                            "collections": [{
                                                "product_id": "time_series"
                                            }]
                                        }
                                    }],
                                }
                            }],
                        }
                    }]
                }
            }
        }

        name, pc = min_time.get_process_list(leaf)
        print(name, pc)


if __name__ == "__main__":
    unittest.main()
