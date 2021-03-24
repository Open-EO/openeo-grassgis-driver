# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import make_response, jsonify

from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema

# Management of user-uploaded assets and processed data.
# need to be uploaded to the actinia server: not supported


class Files(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()

    def get(self):
        response = dict(files=[], links=[])
        return make_response(jsonify(response), 200)


class FilesPath(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()

    def get(self, path):
        # not possible because upload is not supported
        return ErrorSchema(id="1234567890",
                           code=404,
                           message="File <%s> not found" % path).as_response(404)

    def put(self, path):
        # upload is not allowed
        return ErrorSchema(id="1234567890",
                           code=403,
                           message="File upload is not supported").as_response(403)

    def delete(self, path):
        # not possible because upload is not supported
        return ErrorSchema(id="1234567890",
                           code=404,
                           message="File <%s> not found" % path).as_response(404)
