#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) 2019-present mundialis GmbH & Co. KG

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


Basic authentication for using the class Resource from flask_restful.
"""

__author__ = "Anika Bettge"
__copyright__ = "2019-present mundialis GmbH & Co. KG"
__license__ = "Apache-2.0"

# Until now this is only a one-user mockup before ldap integration.

from flask_restful import Resource
from flask import make_response, jsonify, request
import functools
import hashlib
import datetime

from openeo_grass_gis_driver.token_db import TokenDB
from openeo_grass_gis_driver.actinia_processing.config import Config as ActiniaConfig
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema

tokendb = TokenDB()

def ok_user_and_password(username, password):
    iface = ActiniaInterface()
    iface.set_auth(username, password)
    status_code, locations = iface.list_locations()
    if status_code != 200:
        return False
    else:
        return True

def authenticate():
    resp = jsonify({'message': "Unauthorized.", 'status': 401})
    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Main"'
    return resp

# def authenticate_with_token():

def requires_authorization(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers['Authorization']
        auth = auth.split()[1]
        user = tokendb[auth]
        if not user:
            return authenticate()
        return f(*args, **kwargs)
    return decorated

class ResourceBase(Resource):
    decorators = []
    #TODO: fixme
    #decorators.append(requires_authorization)

    def __init__(self):
        Resource.__init__(self)

class Authentication(Resource):
    def get(self):
        auth = request.authorization
        if not auth or not ok_user_and_password(auth.username, auth.password):
            return authenticate()
        hash = hashlib.sha256((ActiniaConfig.SECRET_KEY + auth.username + str(datetime.datetime.now())).encode('UTF-8'))
        hex = hash.hexdigest()
        tokendb[hex] = auth.username
        return make_response(jsonify({
            'user_id': auth.username,
            'access_token': hex
        }), 200)

class OIDCAuthentication(Resource):
    # OpenID Connect https://openid.net/connect/
    def get(self):
        return ErrorSchema(id="1234567890",
                           code=204,
                           message="OpenID Connect is not available").as_response(204)

class UserInfo(Resource):
    def get(self):
        auth = request.authorization
        if not auth or not ok_user_and_password(auth.username, auth.password):
            return ErrorSchema(id="1234567890",
                               code=401,
                               message="Authorization failed").as_response(401)
        
        # user_id, name, storage, budget, links
        # actinia does not provide name, storage, budget, links
        return make_response(jsonify({
            'user_id': auth.username
        }), 200)
        
