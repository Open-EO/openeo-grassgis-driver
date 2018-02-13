# -*- coding: utf-8 -*-
from flask import json
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
        self.base_url = "%(host)s:%(port)s" % {"host": self.host, "port": self.port}
        self.auth = (config.USER, config.PASSWORD)
        self.location = config.LOCATION

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

    def list_mapsets(self):
        url = "%(base)s/locations/%(location)s/mapsets" % {"base": self.base_url,
                                                           "location": self.location}
        return self._send_get_request(url)

    def mapset_info(self, mapset):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/info" % {"base": self.base_url,
                                                                "location": self.location,
                                                                "mapset": mapset}
        return self._send_get_request(url)

    def list_raster(self, mapset):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/raster_layers" % {"base": self.base_url,
                                                                                    "location": self.location,
                                                                                    "mapset": mapset}
        return self._send_get_request(url)

    def list_vector(self, mapset):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/vector_layers" % {"base": self.base_url,
                                                                                    "location": self.location,
                                                                                    "mapset": mapset}
        return self._send_get_request(url)

    def list_strds(self, mapset):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/strds" % {"base": self.base_url,
                                                                            "location": self.location,
                                                                            "mapset": mapset}
        return self._send_get_request(url)

    def strds_info(self, mapset, strds_name):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/strds/%(layer)s" % {"base": self.base_url,
                                                                                      "location": self.location,
                                                                                      "mapset": mapset,
                                                                                      "layer": strds_name}
        return self._send_get_request(url)

    def check_strds_exists(self, strds_name):
        """Return True if the strds exists, False otherwise

        :param strds_name: The name of the strds
        :return: True if the strds exists, False otherwise
        """

        mapset = "PERMANENT"
        if "@" in strds_name:
            strds_name, mapset = strds_name.split("@")

        # Get region information about the required strds and check if it exists
        status_code, strds_info = self.strds_info(mapset=mapset, strds_name=strds_name)

        if status_code != 200:
            return False

        return True
