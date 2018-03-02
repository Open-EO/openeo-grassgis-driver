# -*- coding: utf-8 -*-
from openeo_core.app import flask_api
from graas_openeo_core_wrapper.capabilities import GRaaSCapabilities
from graas_openeo_core_wrapper.data import GRaaSData
from graas_openeo_core_wrapper.data_product_id import GRaaSDataProductId
from graas_openeo_core_wrapper.processes_process_id import GRaaSProcessesProcessId
from graas_openeo_core_wrapper.processes import GRaaSProcesses
from graas_openeo_core_wrapper.jobs import GRaaSJobs
from graas_openeo_core_wrapper.jobs_job_id import GRaaSJobsJobId
from graas_openeo_core_wrapper.udf import GRaaSUdf
from graas_openeo_core_wrapper.udf_lang_udf_type import GRaaSUdfType

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def create_endpoints():
    """Create all endpoints for the openEO Core API GRaaS wrapper

    :return:
    """
    flask_api.add_resource(GRaaSCapabilities, '/capabilities')

    flask_api.add_resource(GRaaSData, '/data')
    flask_api.add_resource(GRaaSDataProductId, '/data/<string:product_id>')

    flask_api.add_resource(GRaaSProcesses, '/processes')
    flask_api.add_resource(GRaaSProcessesProcessId, '/processes/<string:process_id>')

    flask_api.add_resource(GRaaSJobs, '/jobs')
    flask_api.add_resource(GRaaSJobsJobId, '/jobs/<string:job_id>')

    flask_api.add_resource(GRaaSUdf, '/udf')
    flask_api.add_resource(GRaaSUdfType, '/udf/<string:lang>/<string:udf_type>')
