# -*- coding: utf-8 -*-
from flask import make_response, jsonify

from openeo_grass_gis_driver.app import flask_api
from openeo_grass_gis_driver.authentication import \
     Authentication, OIDCAuthentication
from openeo_grass_gis_driver.authentication import UserInfo
from openeo_grass_gis_driver.capabilities import \
     Capabilities, ServiceTypes, Services, CAPABILITIES
from openeo_grass_gis_driver.collections import Collections
from openeo_grass_gis_driver.collection_information import \
     CollectionInformationResource
from openeo_grass_gis_driver.processes import Processes
from openeo_grass_gis_driver.processes_process_id import ProcessesProcessId
from openeo_grass_gis_driver.jobs import Jobs, OutputFormats
from openeo_grass_gis_driver.jobs_job_id import JobsJobId
from openeo_grass_gis_driver.process_graph_validation import GraphValidation
from openeo_grass_gis_driver.result import Result
from openeo_grass_gis_driver.jobs_job_id_estimate import JobsJobIdEstimate
from openeo_grass_gis_driver.jobs_job_id_logs import JobsJobIdLogs
from openeo_grass_gis_driver.jobs_job_id_results import JobsJobIdResults
from openeo_grass_gis_driver.process_graphs import ProcessGraphs
from openeo_grass_gis_driver.process_graphs_id import ProcessGraphId
from openeo_grass_gis_driver.udf import Udf
# from openeo_grass_gis_driver.files import Files, FilesPath
from openeo_grass_gis_driver.well_known import WellKnown

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert, Carmen Tawalika"
__copyright__ = "Copyright 2018-2021, Sören Gebbert, mundialis GmbH & Co. KG"
__maintainer__ = "mundialis"


def add_discovery_endpoints():
    """ Add endpoints to "app" instead of flask_api to bypass URL_PREFIX for
    basic discovery endpoints
    """

    app = flask_api.app

    @app.route('/')
    def index():
        return make_response(jsonify(CAPABILITIES), 200)

    @app.route('/.well-known/openeo')
    def well_known():
        return WellKnown.get(flask_api)


def create_endpoints():
    """Create all endpoints for the openEO Core API wrapper
    """

    add_discovery_endpoints()

    # Capabilities
    flask_api.add_resource(Capabilities, '/')
    flask_api.add_resource(OutputFormats, '/file_formats')
    # /conformance
    flask_api.add_resource(Udf, '/udf_runtimes')
    flask_api.add_resource(ServiceTypes, '/service_types')

    # Account Management
    flask_api.add_resource(OIDCAuthentication, '/credentials/oidc')
    flask_api.add_resource(Authentication, '/credentials/basic')
    flask_api.add_resource(UserInfo, '/me')

    # EO Data Discovery
    flask_api.add_resource(Collections, '/collections')
    flask_api.add_resource(
        CollectionInformationResource,
        '/collections/<string:name>')

    # Predefined Processes
    flask_api.add_resource(Processes, '/processes')
    # /processes/{process_id} is not in API 1.0
    flask_api.add_resource(
        ProcessesProcessId,
        '/processes/<string:process_id>')

    # User-Defined Processes
    flask_api.add_resource(GraphValidation, '/validation')
    flask_api.add_resource(ProcessGraphs, '/process_graphs')
    flask_api.add_resource(ProcessGraphId, '/process_graphs/<string:id>')

    # Data Processing
    # /file_formats listed above in Capabilities
    # /validation listed above in User-Defined Processes
    flask_api.add_resource(Result, '/result')
    flask_api.add_resource(Jobs, '/jobs')
    flask_api.add_resource(JobsJobId, '/jobs/<string:job_id>')
    flask_api.add_resource(JobsJobIdEstimate, '/jobs/<string:job_id>/estimate')
    flask_api.add_resource(JobsJobIdLogs, '/jobs/<string:job_id>/logs')
    flask_api.add_resource(JobsJobIdResults, '/jobs/<string:job_id>/results')

    # Batch Jobs
    # /jobs available in Data Processing
    # /jobs/{job_id} listed above in Data Processing
    # /jobs/{job_id}/estimate listed above in Data Processing
    # /jobs/{job_id}/logs listed above in Data Processing
    # /jobs/{job_id}/results listed above in Data Processing

    # Secondary Services
    # /service_types listed above in Capabilities
    flask_api.add_resource(Services, '/services')
    # /services/{service_id}
    # /services/{service_id}/logs

    # File storage
    # /files
    # /files/{path}
    # flask_api.add_resource(Files, '/files')
    # flask_api.add_resource(FilesPath, '/files/<string:path>')
