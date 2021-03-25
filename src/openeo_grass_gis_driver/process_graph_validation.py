# -*- coding: utf-8 -*-
from flask import make_response, request
from openeo_grass_gis_driver.actinia_processing.base import Graph
from openeo_grass_gis_driver.actinia_processing.config import \
     Config as ActiniaConfig
from openeo_grass_gis_driver.actinia_processing.actinia_interface import \
     ActiniaInterface
from openeo_grass_gis_driver.authentication import ResourceBase
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema
from datetime import datetime

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


# https://api.openeo.org/#operation/validate-custom-process
class GraphValidation(ResourceBase):

    def __init__(self):
        ResourceBase.__init__(self)
        self.iface = ActiniaInterface()
        self.iface.set_auth(ActiniaConfig.USER, ActiniaConfig.PASSWORD)

    def post(self):
        """Run the job in an ephemeral mapset

        :return:
        """

        try:
            # Empty the process location
            ActiniaInterface.PROCESS_LOCATION = {}
            process_graph = request.get_json()

            g = Graph(graph_description=process_graph)
            result_name, process_list = g.to_actinia_process_list()

            if len(
                    ActiniaInterface.PROCESS_LOCATION) == 0 or len(
                    ActiniaInterface.PROCESS_LOCATION) > 1:
                msg = "Processes can only be defined for a single location!"
                status = 400
                es = ErrorSchema(
                    id=str(
                        datetime.now().isoformat()),
                    code=status,
                    message=str(msg))
                return make_response(es.to_json(), status)

            location = ActiniaInterface.PROCESS_LOCATION.keys()
            location = list(location)[0]

            process_chain = dict(list=process_list, version="1")

            status, response = self.iface.sync_ephemeral_processing_validation(
                location=location, process_chain=process_chain)

            if status == 200:
                errors = {"errors": []}
                return make_response(errors, 200)
            else:
                return ErrorSchema(
                    id=str(
                        datetime.now().isoformat()),
                    code=status,
                    message=str(response)).as_response(
                    http_status=status)

        except Exception as e:
            return ErrorSchema(
                id=str(
                    datetime.now().isoformat()),
                code=400,
                message=str(e)).as_response(
                http_status=400)
