# -*- coding: utf-8 -*-
import unittest
import time
import pprint
from flask import json
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.utils.process_graph_examples_v03 import *

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


PREVIEW_TEMPLATE = {
    "process_graph": None,
}


class PreviewTestCase(TestBase):

    def test_graph_filter_bbox_nc_job_ephemeral(self):
        """Run the test in the ephemeral database
        """
        PREVIEW_TEMPLATE["process_graph"] = FILTER_BOX
        response = self.app.post('/preview', data=json.dumps(PREVIEW_TEMPLATE), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)


if __name__ == "__main__":
    unittest.main()
