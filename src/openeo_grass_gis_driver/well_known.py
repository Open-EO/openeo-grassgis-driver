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

        versions = dict()
        versions['0.3.1'] = host_url + "api/v0.3/"
        versions['0.4.0'] = host_url + "api/v0.4/"

        resp = dict()
        resp['versions'] = versions

        return make_response(jsonify(resp), 200)
