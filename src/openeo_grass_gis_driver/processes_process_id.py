# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.authentication import ResourceBase

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessesProcessId(ResourceBase):

    def __init__(self):
        ResourceBase.__init__(self)

    def get(self, process_id):

        if process_id not in PROCESS_DESCRIPTION_DICT:
            return make_response(jsonify({"description": "This process does not exist!"}), 400)

        return make_response(jsonify(PROCESS_DESCRIPTION_DICT[process_id]), 200)
