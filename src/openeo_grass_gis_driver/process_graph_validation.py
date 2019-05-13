# -*- coding: utf-8 -*-
from pprint import pprint
from flask import make_response, request
from openeo_grass_gis_driver.actinia_processing.base import Graph
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.authentication import ResourceBase
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema
from datetime import datetime

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GraphValidation(ResourceBase):

    def __init__(self):
        ResourceBase.__init__(self)
        self.iface = ActiniaInterface()
        self.iface.set_auth(request.authorization.username, request.authorization.password)

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

            if len(ActiniaInterface.PROCESS_LOCATION) == 0 or len(ActiniaInterface.PROCESS_LOCATION) > 1:
                msg = "Processes can only be defined for a single location!"
                status = 400
                es = ErrorSchema(id=str(datetime.now()), code=status, message=str(msg))
                return make_response(es.to_json(), status)

            location = ActiniaInterface.PROCESS_LOCATION.keys()
            location = list(location)[0]

            process_chain = dict(list=process_list,
                                 version="1")

            pprint(process_chain)

            status, response = self.iface.sync_ephemeral_processing_validation(location=location,
                                                                               process_chain=process_chain)
            pprint(response)


            if status == 200:
                return make_response("", 204)
            else:
                es = ErrorSchema(id=str(datetime.now()), code=status, message=str(response))
                return make_response(es.to_json(), status)
        except Exception as e:
                es = ErrorSchema(id=str(datetime.now()), code=400, message=str(e))
                return make_response(es.to_json(), 400)
