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
        self.user = config.USER
        self.location = config.LOCATION

    def check_health(self):

        url = self.base_url + "/health_check"
        r = requests.get(url=url)

        if r.status_code == 200:
            return True

        return False

    def _send_get_request(self, url):
        r = requests.get(url=url, auth=self.auth)
        print(r)
        data = r.text

        if r.status_code == 200:
            ret = r.json()
            data = ret["process_results"]

        return r.status_code, data

    def _send_post_request(self, url, process_chain):
        """Send a post request adn return the return status and the GRaaS response

        :param url:
        :param process_chain:
        :return:
        """
        r = requests.post(url=url, auth=self.auth,
                          json=process_chain)
        data = r.text

        if r.status_code == 200:
            data = r.json()

        return r.status_code, data

    def resource_info(self, resource_id):
        url = "%(base)s/status/%(user)s/%(rid)s" % {"base": self.base_url, "user": self.user, "rid": resource_id}
        r = requests.get(url=url, auth=self.auth)
        data = r.text

        if r.status_code == 200:
            data = r.json()

        return r.status_code, data

    def create_mapset(self, mapset):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s" % {"base": self.base_url,
                                                                      "location": self.location,
                                                                      "mapset": mapset}
        r = requests.post(url=url, auth=self.auth)
        data = r.text

        if r.status_code == 200:
            data = r.json()

        return r.status_code, data

    def delete_mapset(self, mapset):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s" % {"base": self.base_url,
                                                                      "location": self.location,
                                                                      "mapset": mapset}
        r = requests.delete(url=url, auth=self.auth)
        data = r.text

        if r.status_code == 200:
            data = r.json()

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

    def async_persistent_processing(self, mapset, process_chain):
        """Send a process chain to the graas backend to be run asynchronously in a persistent database

        :param mapset: The new mapset to generate
        :param process_chain: The process chain that must be executed
        :return: Status code and the json data (status, json)
        """

        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/processing_async" % {"base": self.base_url,
                                                                                       "location": self.location,
                                                                                       "mapset": mapset}
        return self._send_post_request(url=url, process_chain=process_chain)
