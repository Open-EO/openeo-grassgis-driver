# -*- coding: utf-8 -*-
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

flask_app = Flask(__name__)
CORS(flask_app)
flask_api = Api(flask_app)
