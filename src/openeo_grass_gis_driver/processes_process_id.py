# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import Resource
from openeo_grass_gis_driver.actinia_processing.base import \
     PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.actinia_processing.base import \
    ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT, \
    OPENEO_ACTINIA_ID_DICT
from openeo_grass_gis_driver.actinia_processing.actinia_interface import \
     ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessesProcessId(Resource):

    def __init__(self):
        Resource.__init__(self)

    def get(self, process_id):

        if process_id in PROCESS_DESCRIPTION_DICT:
            return make_response(
                jsonify(
                    PROCESS_DESCRIPTION_DICT[process_id]),
                200)
        elif process_id in ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT:
            iface = ActiniaInterface()
            module = ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT[process_id]

            """ no longer needed because the description in
                ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT is complete

            # get GRASS name for the openeo-like name
            module_name = OPENEO_ACTINIA_ID_DICT[module["id"]]["id"]
            # note that this will list all outputs of a module, not the
            # selected output of the pseudo module
            status_code, module = iface.list_module(module_name)
            if status_code == 200:
                if "parameters" in module:
                    for item in module["parameters"]:
                        if "subtype" in item["schema"]:
                            if item["schema"]["subtype"] in ("cell", "strds"):
                                item["schema"]["type"] = "object"
                                item["schema"]["subtype"] = "raster-cube"
                if "returns" in module:
                    for item in module["returns"]:
                        if "subtype" in item["schema"]:
                            if item["schema"]["subtype"] in ("cell", "strds"):
                                item["schema"]["type"] = "object"
                                item["schema"]["subtype"] = "raster-cube"
            """

            return make_response(jsonify(module), 200)

        return make_response(
            jsonify({"description": "This process does not exist!"}), 400)
