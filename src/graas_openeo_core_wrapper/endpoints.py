# -*- coding: utf-8 -*-
from openeo_core.app import flask_api
from openeo_core.auth_login import AuthLogin
from openeo_core.capabilities import Capabilities
from openeo_core.data import Data
from openeo_core.data_opensearch import DataOpenSearch
from openeo_core.data_product_id import DataProductId
from openeo_core.processes import Processes
from openeo_core.processes_opensearch import ProcessesOpenSearch
from openeo_core.processes_process_id import ProcessesProcessId
from openeo_core.jobs import Jobs
from openeo_core.jobs_job_id import JobsJobId
from openeo_core.jobs_job_id_subscribe import JobsJobIdSubscribe
from openeo_core.jobs_job_id_cancel import JobsJobIdCancel
from openeo_core.download import Download
from openeo_core.udf import Udf
from openeo_core.udf_lang_udf_type import UdfType
from openeo_core.users_user_id_credits import UsersCredits
from openeo_core.users_user_id_files_path import UsersFilesPath
from openeo_core.users_user_id_files import UsersFiles
from openeo_core.users_user_id_jobs import UsersJobs


__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def create_endpoints():
    """Create all endpoints for the openEO Core API

    :return:
    """
    flask_api.add_resource(AuthLogin, '/auth/login')
    flask_api.add_resource(Capabilities, '/capabilities')

    flask_api.add_resource(Data, '/data')
    flask_api.add_resource(DataOpenSearch, '/data/opensearch')
    flask_api.add_resource(DataProductId, '/data/<string:product_id>')

    flask_api.add_resource(Jobs, '/jobs')
    flask_api.add_resource(JobsJobId, '/jobs/<string:job_id>')
    flask_api.add_resource(JobsJobIdCancel, '/jobs/<string:job_id>/cancel')
    flask_api.add_resource(JobsJobIdSubscribe, '/jobs/<string:job_id>/subscribe')

    flask_api.add_resource(Download, '/download/<string:format>/<string:job_id>')

    flask_api.add_resource(Udf, '/udf')
    flask_api.add_resource(UdfType, '/udf/<string:lang>/<string:udf_type>')

    flask_api.add_resource(Processes, '/processes')
    flask_api.add_resource(ProcessesOpenSearch, '/processes/opensearch')
    flask_api.add_resource(ProcessesProcessId, '/processes/<string:process_id>')

    flask_api.add_resource(UsersCredits, '/users/<string:user_id>/credits')
    flask_api.add_resource(UsersFilesPath, '/users/<string:user_id>/files/<string:path>')
    flask_api.add_resource(UsersFiles, '/users/<string:user_id>/files')
    flask_api.add_resource(UsersJobs, '/users/<string:user_id>/jobs')


