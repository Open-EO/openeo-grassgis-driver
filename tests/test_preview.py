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
        """Test the filter box process
        """
        PREVIEW_TEMPLATE["process_graph"] = FILTER_BOX
        response = self.app.post('/preview', data=json.dumps(PREVIEW_TEMPLATE), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_filter_bbox_nc_job_ephemeral_error(self):
        """Test the filter box process that produces an error because of wrong raster name
        """

        fbox = FILTER_BOX
        fbox["process_graph"]["imagery"]["data_id"] = "nc_spm_08.PERMANENT.raster.elevation_nonon"
        PREVIEW_TEMPLATE["process_graph"] = fbox
        response = self.app.post('/preview', data=json.dumps(PREVIEW_TEMPLATE), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(400, response.status_code)

    def test_graph_get_data_1(self):
        """Test the get data process to get raster data
        """
        PREVIEW_TEMPLATE["process_graph"] = GET_DATA_1
        response = self.app.post('/preview', data=json.dumps(PREVIEW_TEMPLATE), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_get_data_3(self):
        """Test the get data process to get strds data
        """
        PREVIEW_TEMPLATE["process_graph"] = GET_DATA_3
        response = self.app.post('/preview', data=json.dumps(PREVIEW_TEMPLATE), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_daterange(self):
        """Run the daterange process
        """
        PREVIEW_TEMPLATE["process_graph"] = DATERANGE
        response = self.app.post('/preview', data=json.dumps(PREVIEW_TEMPLATE), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_raster_export(self):
        """Run the raster export process
        """
        PREVIEW_TEMPLATE["process_graph"] = RASTER_EXPORT
        response = self.app.post('/preview', data=json.dumps(PREVIEW_TEMPLATE), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_raster_zonal_statistics_single(self):
        """Run the zonal statistics process
        """
        PREVIEW_TEMPLATE["process_graph"] = ZONAL_STATISTICS_SINGLE
        response = self.app.post('/preview', data=json.dumps(PREVIEW_TEMPLATE), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
