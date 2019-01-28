# -*- coding: utf-8 -*-
from openeo_grass_gis_driver.app import flask_api
from openeo_grass_gis_driver.capabilities import Capabilities, ServiceTypes
from openeo_grass_gis_driver.collections import Collections
from openeo_grass_gis_driver.collection_information import CollectionInformationResource
from openeo_grass_gis_driver.processes import Processes
from openeo_grass_gis_driver.jobs import Jobs, OutputFormats
from openeo_grass_gis_driver.jobs_job_id import JobsJobId
from openeo_grass_gis_driver.process_graph_validation import GraphValidation
from openeo_grass_gis_driver.preview import Preview
from openeo_grass_gis_driver.jobs_job_id_results import JobsJobIdResults
from openeo_grass_gis_driver.process_graphs import ProcessGraphs
from openeo_grass_gis_driver.process_graphs_id import ProcessGraphId

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def create_endpoints():
    """Create all endpoints for the openEO Core API  wrapper
    """
    flask_api.add_resource(Capabilities, '/')
    flask_api.add_resource(ServiceTypes, '/service_types')

    flask_api.add_resource(Collections, '/collections')
    flask_api.add_resource(CollectionInformationResource, '/collections/<string:name>')

    flask_api.add_resource(Processes, '/processes')

    flask_api.add_resource(GraphValidation, '/validation')
    flask_api.add_resource(Preview, '/preview')
    flask_api.add_resource(ProcessGraphs, '/process_graphs')
    flask_api.add_resource(ProcessGraphId, '/process_graphs/<string:process_graph_id>')

    flask_api.add_resource(OutputFormats, '/output_formats')
    flask_api.add_resource(Jobs, '/jobs')
    flask_api.add_resource(JobsJobId, '/jobs/<string:job_id>')
    flask_api.add_resource(JobsJobIdResults, '/jobs/<string:job_id>/results')

