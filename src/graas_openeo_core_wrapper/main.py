# -*- coding: utf-8 -*-
from openeo_core.app import flask_app
from graas_openeo_core_wrapper.endpoints import create_endpoints

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


if __name__ == '__main__':
    create_endpoints()
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
