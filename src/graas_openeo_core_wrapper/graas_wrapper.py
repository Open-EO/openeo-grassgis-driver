# -*- coding: utf-8 -*-
from flask import json
from openeo_core.app import flask_app
from graas_openeo_core_wrapper.config import Config as GRaaSConfig
import requests

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 20186, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class GRaaSInterface(object):

    def __init__(self, config=None):

        if config is None:
            config = GRaaSConfig

        self.host = config.HOST
        self.port = config.PORT
        self.base_url = "%(host)s:%(port)s"%{"host":self.host, "port":self.port}
        self.auth = (config.USER, config.PASSWORD)
        self.location = config.LOCATION
        self.mapset = config.MAPSET

    def check_health(self):

        url = self.base_url + "/health_check"
        print(url)
        r = requests.get(url=url)

        if r.status_code == 200:
            return True

        return False

    def _send_get_request(self, url):
        r = requests.get(url=url, auth=self.auth)
        print(r)
        data = None

        if r.status_code == 200:
            ret = json.loads(r.text)
            data = ret["process_results"]

        return r.status_code, data

    def list_raster(self):
        url = "%(base)s/locations/%(loc)s/mapsets/%(map)s/raster_layers"%{"base":self.base_url,
                                                                          "loc":self.location,
                                                                          "map":self.mapset}
        return self._send_get_request(url)

    def list_vector(self):
        url = "%(base)s/locations/%(loc)s/mapsets/%(map)s/vector_layers"%{"base":self.base_url,
                                                                          "loc":self.location,
                                                                          "map":self.mapset}
        return self._send_get_request(url)

    def list_strds(self):
        url = "%(base)s/locations/%(loc)s/mapsets/%(map)s/strds"%{"base":self.base_url,
                                                                          "loc":self.location,
                                                                          "map":self.mapset}
        return self._send_get_request(url)
