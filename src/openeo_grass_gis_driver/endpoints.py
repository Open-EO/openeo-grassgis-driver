# -*- coding: utf-8 -*-
from .app import flask_api
from .capabilities import GRaaSCapabilities
from .data import GRaaSData
from .data_product_id import GRaaSDataProductId
from .processes_process_id import GRaaSProcessesProcessId
from .processes import GRaaSProcesses
from .jobs import GRaaSJobs
from .jobs_job_id import GRaaSJobsJobId
from .udf import GRaaSUdf
from .udf_lang_udf_type import GRaaSUdfType

__license__ = "Apache License, Version 2.0"
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
