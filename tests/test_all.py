# -*- coding: utf-8 -*-
import json
import sys
import unittest
from openeo_core.auth_login import AuthLogin, AUTH_LOGIN_EXAMPLE
from openeo_core.capabilities import Capabilities, GET_CAPABILITIES_EXAMPLE
from openeo_core.data import Data, GET_DATA_EXAMPLE
from openeo_core.data_opensearch import DataOpenSearch, GET_DATA_OPENSEARCH_EXAMPLE
from openeo_core.data_product_id import DataProductId, GET_DATA_PRODUCT_ID_EXAMPLE
from openeo_core.processes import Processes, GET_PROCESSES_EXAMPLE
from openeo_core.processes_opensearch import ProcessesOpenSearch, GET_PROCESSES_OPENSEARCH_EXAMPLE
from openeo_core.processes_process_id import ProcessesProcessId, GET_PROCESSES_PROCESS_ID_EXAMPLE
from openeo_core.jobs import Jobs, POST_JOBS_EXAMPLE
from openeo_core.jobs_job_id import JobsJobId, DELETE_JOBS_ID_EXAMPLE
from openeo_core.definitions import Job
from openeo_core.jobs_job_id_cancel import GET_JOBS_ID_CANCEL_EXAMPLE
from openeo_core.jobs_job_id_subscribe import JobsJobIdSubscribe, GET_JOBS_ID_SUB_EXAMPLE
from openeo_core.download import Download, GET_DOWNLOAD_EXAMPLE
from openeo_core.udf import Udf, GET_UDF_EXAMPLE
from openeo_core.udf_lang_udf_type import UdfType, GET_UDF_TYPE_EXAMPLE
from openeo_core.users_user_id_credits import UsersCredits, GET_USERS_CREDITS_EXAMPLE
from openeo_core.users_user_id_files_path import UsersFilesPath, GET_USERS_FILES_PATH_EXAMPLE,\
    PUT_USERS_FILES_PATH_EXAMPLE, DELETE_USERS_FILES_PATH_EXAMPLE
from openeo_core.users_user_id_files import UsersFiles, GET_USERS_FILES_EXAMPLE
from openeo_core.users_user_id_jobs import UsersJobs, GET_USERS_JOBS_EXAMPLE

from openeo_core.app import flask_api
from openeo_core.endpoints import create_endpoints

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class AllTestCase(unittest.TestCase):

    create_endpoints()

    def setUp(self):
        self.app = flask_api.app.test_client()

    def test_auth_login(self):
        response = self.app.get('/auth/login')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         AUTH_LOGIN_EXAMPLE)

    def test_capabilities(self):
        response = self.app.get('/capabilities')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         GET_CAPABILITIES_EXAMPLE)

    def test_data(self):
        response = self.app.get('/data')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         GET_DATA_EXAMPLE)

    def test_data_opensearch(self):
        response = self.app.get('/data/opensearch')
        print(response.data)

        self.assertEqual(response.data.decode(),
                         GET_DATA_OPENSEARCH_EXAMPLE)

    def test_data_product_id(self):
        response = self.app.get('/data/1')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         GET_DATA_PRODUCT_ID_EXAMPLE)

    def test_jobs(self):
        response = self.app.post('/jobs')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         POST_JOBS_EXAMPLE)

    def test_jobs_get_job_id(self):
        response = self.app.get('/jobs/1')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         Job.example)

    def test_jobs_delete_job_id(self):
        response = self.app.delete('/jobs/1')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         DELETE_JOBS_ID_EXAMPLE)

    def test_jobs_job_id_cancel(self):
        response = self.app.get('/jobs/1/cancel')
        print(response.data)

        self.assertEqual(json.loads(response.data.decode()),
                         GET_JOBS_ID_CANCEL_EXAMPLE)

    def test_jobs_job_id_subscribe(self):
        response = self.app.get('/jobs/1/subscribe')
        print(response.data)

        self.assertEqual(response.data.decode(),
                         GET_JOBS_ID_SUB_EXAMPLE)

    def test_download(self):
        response = self.app.get('/download/format/job_id')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         GET_DOWNLOAD_EXAMPLE)

    def test_udf(self):
        response = self.app.get('/udf')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         GET_UDF_EXAMPLE)

    def test_udf_lang_udf_type(self):
        response = self.app.get('/udf/python/time_series_aggregation')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         GET_UDF_TYPE_EXAMPLE)

    def test_processes(self):
        response = self.app.get('/processes')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         GET_PROCESSES_EXAMPLE)

    def test_processes_opensearch(self):
        response = self.app.get('/processes/opensearch')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         GET_PROCESSES_OPENSEARCH_EXAMPLE)

    def test_processes_process_id(self):
        response = self.app.get('/processes/1')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         GET_PROCESSES_PROCESS_ID_EXAMPLE)

    def test_users_credits(self):
        response = self.app.get('/users/soeren/credits')
        print(response.data)
        self.assertEqual(response.data.decode(),
                         GET_USERS_CREDITS_EXAMPLE)

    def test_users_files_path(self):
        response = self.app.get('/users/soeren/files/elevation.tif')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         GET_USERS_FILES_PATH_EXAMPLE)

        response = self.app.put('/users/soeren/files/elevation.tif')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         PUT_USERS_FILES_PATH_EXAMPLE)

        response = self.app.delete('/users/soeren/files/elevation.tif')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         DELETE_USERS_FILES_PATH_EXAMPLE)

    def test_users_files(self):
        response = self.app.get('/users/soeren/files')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         GET_USERS_FILES_EXAMPLE)

    def test_users_jobs(self):
        response = self.app.get('/users/soeren/jobs')
        print(response.data)
        self.assertEqual(json.loads(response.data.decode()),
                         GET_USERS_JOBS_EXAMPLE)


if __name__ == "__main__":
    unittest.main()
