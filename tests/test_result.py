# -*- coding: utf-8 -*-
import unittest
import time
import pprint
from flask import json
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.utils.process_graph_examples_v04 import *


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class PreviewTestCase(TestBase):

    def test_graph_bbox_from_raster_nc_job_ephemeral(self):
        """Test the bbox from raster process
        """
        response = self.app.post('/result', data=json.dumps(BBOX_FROM_RASTER), content_type="application/json", headers=self.auth)

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_filter_bbox_nc_job_ephemeral(self):
        """Test the filter box process
        """
        response = self.app.post('/result', data=json.dumps(FILTER_BBOX), content_type="application/json", headers=self.auth)

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_filter_bbox_nc_job_ephemeral_error(self):
        """Test the filter box process that produces an error because of wrong raster name
        """

        fbox = FILTER_BBOX
        fbox["process_graph"]["get_data_1"]["arguments"]["id"] = "nc_spm_08.PERMANENT.raster.elevation_nonon"
        response = self.app.post('/result', data=json.dumps(fbox), content_type="application/json", headers=self.auth)

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(400, response.status_code)

    def test_graph_get_data_1(self):
        """Test the get data process to get raster data
        """
        response = self.app.post('/result', data=json.dumps(GET_DATA_1), content_type="application/json", headers=self.auth)

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_get_data_3(self):
        """Test the get data process to get strds data
        """
        response = self.app.post('/result', data=json.dumps(GET_DATA_3), content_type="application/json", headers=self.auth)

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_daterange(self):
        """Run the daterange process
        """
        response = self.app.post('/result', data=json.dumps(DATERANGE), content_type="application/json", headers=self.auth)

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_raster_export(self):
        """Run the raster export process
        """
        response = self.app.post('/result', data=json.dumps(RASTER_EXPORT), content_type="application/json", headers=self.auth)

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_rgb_raster_export(self):
        """Run the rgb raster export process
        """
        response = self.app.post('/result', data=json.dumps(RGB_RASTER_EXPORT), content_type="application/json", headers=self.auth)

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_raster_zonal_statistics(self):
        """Run the zonal statistics process
        """
        response = self.app.post('/result', data=json.dumps(ZONAL_STATISTICS), content_type="application/json", headers=self.auth)

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)

    def test_graph_map_algebra(self):
        """Run the map algebra process
        """
        response = self.app.post('/result', data=json.dumps(MAP_ALGEBRA), content_type="application/json", headers=self.auth)

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
