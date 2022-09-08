# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import make_response, jsonify, request


__license__ = "Apache License, Version 2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "2018-2021 mundialis GmbH & Co. KG"


API_VERSION = "1.0.1"
API_SHORT_VERSION = "v%s.%s" % (
    API_VERSION.split('.')[0], API_VERSION.split('.')[1])
# This is the URL prefix that is used by app.py and must be used in the tests
URL_PREFIX = "/api/%s" % API_SHORT_VERSION


class WellKnown(Resource):

    def __init__(self):
        Resource.__init__(self)

    def get(self):

        url = '%s%s/' % (request.root_url.strip('/'), URL_PREFIX)

        version_list = list()
        version_list.append({"url": url,
                             "api_version": API_VERSION,
                             "production": False})

        resp = dict()
        resp['versions'] = version_list

        return make_response(jsonify(resp), 200)
