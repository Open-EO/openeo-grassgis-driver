# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import make_response, jsonify
from openeo_grass_gis_driver.actinia_processing.base import \
    ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT, PROCESS_DESCRIPTION_DICT

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class Processes(Resource):

    def __init__(self):
        Resource.__init__(self)

    def get(self):

        # can have a query parameter 'limit' to enable pagination
        # get the value of limit (i.e. ?limit=10)
        # limit = request.args.get('limit')

        pd_list = list()
        for key in PROCESS_DESCRIPTION_DICT:
            pd = PROCESS_DESCRIPTION_DICT[key]
            pd_list.append(pd)
        for key in ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT:
            pd = ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT[key]
            pd_list.append(pd)

        response = dict(processes=pd_list, links=[])

        return make_response(jsonify(response), 200)
