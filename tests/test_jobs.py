# -*- coding: utf-8 -*-
import unittest
import time
import pprint
from flask import json
from openeo_grass_gis_driver.test_base import TestBase
from openeo_grass_gis_driver.actinia_processing import config
from openeo_grass_gis_driver.utils.process_graph_examples_v03 import *

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


JOB_TEMPLATE = {
    "title": "The title of the job",
    "description": "The description of the job",
    "process_graph": None,
}

class JobsTestCase(TestBase):

    def test_graph_filter_bbox_nc_job_ephemeral(self):
        """Run the test in the ephemeral database
        """
        JOB_TEMPLATE["process_graph"] = FILTER_BOX
        response = self.app.post('/jobs', data=json.dumps(JOB_TEMPLATE), content_type="application/json")

        data = json.loads(response.data.decode())
        pprint.pprint(data)

        self.wait_until_finished(response)

    def wait_until_finished(self, response, http_status=200, status="finished"):
        """Poll the status of a resource and assert its finished HTTP status

        The response will be checked if the resource was accepted. Hence it must always be HTTP 200 status.

        The status URL from the response is then polled until status: finished, error or terminated.
        The result of the poll can be checked against its HTTP status and its GRaaS status message.

        Args:
            response: The accept response
            http_status (int): The HTTP status that should be checked
            status (str): The return status of the response

        Returns: response

        """
        # Check if the resource was accepted
        self.assertEqual(response.status_code, 200, "HTML status code is wrong %i" % response.status_code)
        self.assertEqual(response.mimetype, "application/json", "Wrong mimetype %s" % response.mimetype)

        resp_data = json.loads(response.data.decode())

        while True:
            print("waiting for finished job")
            response = self.app.get('/jobs/%s' % resp_data["job_id"])
            resp_data = json.loads(response.data.decode())
            print(response)
            print(resp_data)

            if "status" not in resp_data:
                raise Exception("wrong return values %s" % str(resp_data))
            if resp_data["status"] == "finished" or \
                    resp_data["status"] == "error" or \
                    resp_data["status"] == "terminated":
                break
            time.sleep(0.2)

        self.assertEqual(resp_data["status"], status)
        self.assertEqual(response.status_code, http_status, "HTML status code is wrong %i" % response.status_code)

        time.sleep(0.4)
        pprint.pprint(resp_data)
        return resp_data


if __name__ == "__main__":
    unittest.main()
