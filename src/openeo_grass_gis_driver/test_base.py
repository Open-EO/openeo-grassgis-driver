# -*- coding: utf-8 -*-
import unittest
from flask import json
import time
from openeo_grass_gis_driver.app import flask_api
from openeo_grass_gis_driver.endpoints import create_endpoints
from openeo_grass_gis_driver.actinia_processing.config import Config as ActiniaConfig

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class TestBase(unittest.TestCase):

    create_endpoints()

    def setUp(self):
        self.app = flask_api.app.test_client()
        self.gconf = ActiniaConfig()
        self.gconf.PORT = "443"

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
        return resp_data
