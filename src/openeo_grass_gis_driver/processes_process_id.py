# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import Resource
from openeo_grass_gis_driver.actinia_processing.base import \
     PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.actinia_processing.base import \
    ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT

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
            # the description in ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT
            # must be complete and correct
            module = ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT[process_id]

            return make_response(jsonify(module), 200)

        return make_response(
            jsonify({"description": "This process does not exist!"}), 400)
