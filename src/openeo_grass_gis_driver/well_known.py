# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import make_response, jsonify, request


__license__ = "Apache License, Version 2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "2018-present mundialis GmbH & Co. KG"


class WellKnown(Resource):

    def __init__(self):
        Resource.__init__(self)

    def get(self):

        host_url = request.host_url

        version_list = list()
        version_list.append({"url": host_url + "api/v0.3/",
                             "api_version": "0.3.1",
                             "production": False})
        version_list.append({"url": host_url + "api/v0.4/",
                             "api_version": "0.4.0",
                             "production": False})
        version_list.append({"url": host_url + "api/v1.0/",
                             "api_version": "1.0.0",
                             "production": False})

        resp = dict()
        resp['versions'] = version_list

        return make_response(jsonify(resp), 200)
