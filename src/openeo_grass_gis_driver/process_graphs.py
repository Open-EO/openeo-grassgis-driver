# -*- coding: utf-8 -*-
from uuid import uuid4
import traceback
import sys
from datetime import datetime
from flask import make_response, jsonify, request
from flask_restful import Resource
from openeo_grass_gis_driver.process_graph_db import GraphDB
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphListEntry, ProcessGraphList
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessGraphs(Resource):
    """The /jobs endpoint implementation"""

    def __init__(self):
        self.iface = ActiniaInterface()
        self.graph_db = GraphDB()

    def get(self):
        """Return all jobs in the job database"""
        # TODO: Implement user specific database access

        process_graphs = []

        for key in self.graph_db:
            graph = self.graph_db[key]

            entry = ProcessGraphListEntry(title=graph["title"], description=graph["description"], id=key)

            process_graphs.append(entry)

        return make_response(ProcessGraphList(process_graphs=process_graphs).to_json(), 200)

    def post(self):
        try:
            """Store a process graph in the graph database"""
            # TODO: Implement user specific database access

            process_graph_id = f"user-graph::{str(uuid4())}"

            process_graph = request.get_json()
            self.graph_db[process_graph_id] = process_graph

            return make_response(process_graph_id, 201)
        except Exception:

            e_type, e_value, e_tb = sys.exc_info()
            traceback_model = dict(message=str(e_value),
                                   traceback=traceback.format_tb(e_tb),
                                   type=str(e_type))
            error = ErrorSchema(id="1234567890", code=2, message=str(traceback_model))
            return make_response(error.to_json(), 400)

    def delete(self):
        """Clear the process graph database"""
        self.graph_db.clear()
        return make_response("All process graphs have been successfully deleted", 204)
