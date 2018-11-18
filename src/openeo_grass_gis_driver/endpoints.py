# -*- coding: utf-8 -*-
from .app import flask_api
from .capabilities import Capabilities, OutputFormats, ServiceTypes
from .collections import Collections
from .collection_information import CollectionInformationResource
from .processes import Processes
from .jobs import Jobs
from .jobs_job_id import JobsJobId
from .graph_validation import GraphValidation

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def create_endpoints():
    """Create all endpoints for the openEO Core API  wrapper

    :return:
    """
    flask_api.add_resource(Capabilities, '/')
    flask_api.add_resource(OutputFormats, '/output_formats')
    flask_api.add_resource(ServiceTypes, '/service_types')

    flask_api.add_resource(Collections, '/collections')
    flask_api.add_resource(CollectionInformationResource, '/collections/<string:name>')

    flask_api.add_resource(Processes, '/processes')
    flask_api.add_resource(GraphValidation, '/validation')

    # flask_api.add_resource(Jobs, '/jobs')
    # flask_api.add_resource(JobsJobId, '/jobs/<string:job_id>')
