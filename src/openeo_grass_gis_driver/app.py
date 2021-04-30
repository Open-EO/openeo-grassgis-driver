# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from werkzeug.middleware.proxy_fix import ProxyFix

from openeo_grass_gis_driver.well_known import URL_PREFIX


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert, Carmen Tawalika"
__copyright__ = "Copyright 2018-2021, Sören Gebbert, mundialis"
__maintainer__ = "mundialis"


flask_app = Flask(__name__)
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_for=1, x_host=1, x_proto=1)
# CORS(flask_app, supports_credentials=True)
CORS(flask_app)
flask_api = Api(flask_app, prefix=URL_PREFIX)
