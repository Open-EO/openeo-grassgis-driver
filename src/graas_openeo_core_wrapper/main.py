# -*- coding: utf-8 -*-
from openeo_core.app import flask_app
from graas_openeo_core_wrapper.endpoints import create_endpoints

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

if __name__ == '__main__':
    create_endpoints()
    flask_app.run(debug=True)
