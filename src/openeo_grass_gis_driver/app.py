# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from werkzeug.middleware.proxy_fix import ProxyFix

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

flask_app = Flask(__name__)
flask_app.wsgi_app = ProxyFix(flask_app.wsgi_app, x_for=1, x_host=1, x_proto=1)
# as flaks CORS lead to unforeseen behaviour in certain cases, we configure
# headers with nginx and outcomment here.
# CORS(flask_app, supports_credentials=True)
flask_api = Api(flask_app)
