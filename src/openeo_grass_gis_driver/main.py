# -*- coding: utf-8 -*-
from openeo_grass_gis_driver.app import flask_app
from openeo_grass_gis_driver.endpoints import create_endpoints


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


if __name__ == '__main__':
    create_endpoints()
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
