# -*- coding: utf-8 -*-
from openeo_grass_gis_driver.app import flask_app
from openeo_grass_gis_driver.endpoints import create_endpoints
from openeo_grass_gis_driver.register_actinia_processes import \
    register_processes


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert, Carmen Tawalika"
__copyright__ = "Copyright 2018-2021, Sören Gebbert, mundialis"
__maintainer__ = "mundialis"


register_processes()
create_endpoints()

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', port=5000, debug=True)
