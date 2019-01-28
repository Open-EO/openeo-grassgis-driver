# -*- coding: utf-8 -*-
from uuid import uuid4
from datetime import datetime
from flask import make_response, jsonify, request
from flask_restful import Resource
from openeo_grass_gis_driver.process_graph_db import GraphDB
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.process_graph_schemas import ProcessGraphListEntry, ProcessGraphList
from openeo_grass_gis_driver.error_schemas import ErrorSchema

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessGraphId(Resource):
    """The /jobs endpoint implementation"""

    def __init__(self):
        self.iface = ActiniaInterface()
        self.graph_db = GraphDB()

    def get(self, process_graph_id):
        """Return all jobs in the job database"""
        # TODO: Implement user specific database access

        if process_graph_id in self.graph_db:

            graph = self.graph_db[process_graph_id]
            graph["process_graph_id"] = process_graph_id
            return make_response(jsonify(graph), 200)
        else:
            return make_response(ErrorSchema(id=str(uuid4()), code=400,
                                             message=f"Process graph id {process_graph_id} not found").to_json(), 400)
