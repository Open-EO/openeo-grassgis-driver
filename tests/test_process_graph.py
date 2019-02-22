# -*- coding: utf-8 -*-
import unittest
import pprint
from flask import json
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.utils.process_graph_examples_v03 import *

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


PROCESS_CHAIN_TEMPLATE = {
    "title": "The title of the process chain",
    "description": "The description of the process chain",
    "process_graph": None,
}


class ProcessGraphTestCase(TestBase):

    def setUp(self):
        TestBase.setUp(self)
        response = self.app.delete('/process_graphs', headers=self.auth)
        self.assertEqual(204, response.status_code)

    def test_job_creation_1(self):
        """Run the test in the ephemeral database
        """
        PROCESS_CHAIN_TEMPLATE["process_graph"] = FILTER_BOX["process_graph"]

        response = self.app.post('/process_graphs', data=json.dumps(PROCESS_CHAIN_TEMPLATE),
                                 content_type="application/json", headers=self.auth)
        self.assertEqual(201, response.status_code)
        process_graph_id = response.get_data().decode("utf-8")

        response = self.app.get('/process_graphs', headers=self.auth)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.get_data().decode("utf-8"))
        pprint.pprint(data)

        self.assertEqual(process_graph_id, data["process_graphs"][0]["process_graph_id"])

        response = self.app.get(f'/process_graphs/{process_graph_id}', headers=self.auth)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.get_data().decode("utf-8"))
        pprint.pprint(data)

        self.assertEqual(process_graph_id, data["process_graph_id"])
        self.assertEqual(FILTER_BOX["process_graph"], data["process_graph"])


    def test_job_creation_2(self):
        """Run the test in the ephemeral database
        """
        PROCESS_CHAIN_TEMPLATE["process_graph"] = FILTER_BOX["process_graph"]

        response = self.app.post('/process_graphs', data=json.dumps(PROCESS_CHAIN_TEMPLATE),
                                 content_type="application/json", headers=self.auth)
        self.assertEqual(201, response.status_code)
        process_graph_id = response.get_data().decode("utf-8")

        response = self.app.get(f'/process_graphs/{process_graph_id}', headers=self.auth)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.get_data().decode("utf-8"))
        pprint.pprint(data)

        self.assertEqual(process_graph_id, data["process_graph_id"])
        self.assertEqual(FILTER_BOX["process_graph"], data["process_graph"])

        response = self.app.delete(f'/process_graphs/{process_graph_id}', headers=self.auth)
        self.assertEqual(204, response.status_code)

        response = self.app.get(f'/process_graphs/{process_graph_id}', headers=self.auth)
        self.assertEqual(400, response.status_code)

        response = self.app.get('/process_graphs', headers=self.auth)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.get_data().decode("utf-8"))
        pprint.pprint(data)

        self.assertEqual(0, len(data['process_graphs']))

    def test_job_creation_3(self):
        """Run the test in the ephemeral database
        """
        PROCESS_CHAIN_TEMPLATE["process_graph"] = FILTER_BOX["process_graph"]

        # Create graph
        response = self.app.post('/process_graphs', data=json.dumps(PROCESS_CHAIN_TEMPLATE),
                                 content_type="application/json", headers=self.auth)
        self.assertEqual(201, response.status_code)
        process_graph_id = response.get_data().decode("utf-8")

        # Check graph
        response = self.app.get(f'/process_graphs/{process_graph_id}', headers=self.auth)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.get_data().decode("utf-8"))
        pprint.pprint(data)

        self.assertEqual(process_graph_id, data["process_graph_id"])
        self.assertEqual(FILTER_BOX["process_graph"], data["process_graph"])

        # Modify graph
        PROCESS_CHAIN_TEMPLATE["process_graph"] = ZONAL_STATISTICS_SINGLE["process_graph"]

        response = self.app.patch(f'/process_graphs/{process_graph_id}',
                                  data=json.dumps(PROCESS_CHAIN_TEMPLATE),
                                  content_type="application/json", headers=self.auth)
        self.assertEqual(204, response.status_code)

        # Check graph
        response = self.app.get(f'/process_graphs/{process_graph_id}', headers=self.auth)
        self.assertEqual(200, response.status_code)

        data = json.loads(response.get_data().decode("utf-8"))
        pprint.pprint(data)

        self.assertEqual(process_graph_id, data["process_graph_id"])
        self.assertEqual(ZONAL_STATISTICS_SINGLE["process_graph"], data["process_graph"])


if __name__ == "__main__":
    unittest.main()
