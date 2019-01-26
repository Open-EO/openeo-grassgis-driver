# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import Resource
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DESCRIPTION_DICT_LEGACY

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class Processes(Resource):

    def get(self):

        pd_list = list()
        for key in PROCESS_DESCRIPTION_DICT_LEGACY:
            pd = PROCESS_DESCRIPTION_DICT_LEGACY[key]
            pd_list.append(pd)

        response = dict(processes=pd_list, links=[])

        return make_response(jsonify(response), 200)
