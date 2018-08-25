# -*- coding: utf-8 -*-
from .config import Config as ActiniaConfig
import requests

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ActiniaInterface(object):
    """
    This is the interface class to the actinia REST service that uses GRASS GIS as backend
    """

    PROCESS_LOCATION = {}

    def __init__(self, config=None):

        if config is None:
            config = ActiniaConfig

        self.host = config.HOST
        self.port = config.PORT
        self.base_url = "%(host)s:%(port)s/latest" % {"host": self.host, "port": self.port}
        self.auth = (config.USER, config.PASSWORD)
        self.user = config.USER

    @staticmethod
    def layer_def_to_components(layer):
        """Convert the name of a layer in the openeo framework into GRASS GIS definitions

        location.mapset.datatype.layer -> (location, mapset, datatype, layer)

        Return (None, None, None, layer) if no location/mapset information was found

        :param layer: The name of the layer in the form location.mapset.layer
        :return: (location, mapset, datatype, layer) or (None, None, None, layer)
        """

        if layer.count(".") < 3:
            return None, None, None, layer

        location, mapset, datatype, layer = layer.split(".", 3)

        # Store the location in the global location dict
        ActiniaInterface.PROCESS_LOCATION[location] = location

        return location, mapset, datatype, layer

    def check_health(self):

        url = self.base_url + "/health_check"
        r = requests.get(url=url)

        if r.status_code == 200:
            return True

        return False

    def _send_get_request(self, url):
        r = requests.get(url=url, auth=self.auth)
        data = r.text

        if r.status_code == 200:
            ret = r.json()
            data = ret["process_results"]

        return r.status_code, data

    def _send_post_request(self, url, process_chain):
        """Send a post request and return the return status and the Actinia response

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
        url = "%(base)s/resources/%(user)s/%(rid)s" % {"base": self.base_url, "user": self.user, "rid": resource_id}
        r = requests.get(url=url, auth=self.auth)
        data = r.text

        if r.status_code == 200:
            data = r.json()

        return r.status_code, data

    def delete_resource(self, resource_id):
        url = "%(base)s/resources/%(user)s/%(rid)s" % {"base": self.base_url, "user": self.user, "rid": resource_id}
        r = requests.delete(url=url, auth=self.auth)
        data = r.text

        if r.status_code == 200:
            data = r.json()

        return r.status_code, data

    def create_mapset(self, location, mapset="PERMANENT"):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s" % {"base": self.base_url,
                                                                      "location": location,
                                                                      "mapset": mapset}
        r = requests.post(url=url, auth=self.auth)
        data = r.text

        if r.status_code == 200:
            data = r.json()

        return r.status_code, data

    def delete_mapset(self, location, mapset="PERMANENT"):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s" % {"base": self.base_url,
                                                                      "location": location,
                                                                      "mapset": mapset}
        r = requests.delete(url=url, auth=self.auth)
        data = r.text

        if r.status_code == 200:
            data = r.json()

        return r.status_code, data

    def list_mapsets(self, location):
        url = "%(base)s/locations/%(location)s/mapsets" % {"base": self.base_url,
                                                           "location": location}
        return self._send_get_request(url)

    def mapset_info(self, location, mapset):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/info" % {"base": self.base_url,
                                                                           "location": location,
                                                                           "mapset": mapset}
        return self._send_get_request(url)

    def list_raster(self, location, mapset):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/raster_layers" % {"base": self.base_url,
                                                                                    "location": location,
                                                                                    "mapset": mapset}
        return self._send_get_request(url)

    def list_vector(self, location, mapset):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/vector_layers" % {"base": self.base_url,
                                                                                    "location": location,
                                                                                    "mapset": mapset}
        return self._send_get_request(url)

    def list_strds(self, location, mapset):
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/strds" % {"base": self.base_url,
                                                                            "location": location,
                                                                            "mapset": mapset}
        return self._send_get_request(url)

    def layer_info(self, layer_name):
        """Return informations about the requested layer, that can be of type raster, vector or strds

        :param layer_name:
        :return:
        """
        location, mapset, datatype, layer = ActiniaInterface.layer_def_to_components(layer_name)
        if datatype == "raster":
            datatype = "raster_layers"
        if datatype == "vector":
            datatype = "vector_layers"
        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/%(dtype)s/%(layer)s" % {"base": self.base_url,
                                                                                          "location": location,
                                                                                          "mapset": mapset,
                                                                                          "dtype": datatype,
                                                                                          "layer": layer}
        return self._send_get_request(url)

    def check_layer_exists(self, layer_name):
        """Return True if the strds exists, False otherwise

        :param strds_name: The name of the strds
        :return: True if the strds exists, False otherwise
        """
        # Get region information about the required strds and check if it exists
        status_code, layer_info = self.layer_info(layer_name=layer_name)

        if status_code != 200:
            return False

        return True

    def async_persistent_processing(self, location, mapset, process_chain):
        """Send a process chain to the Actinia backend to be run asynchronously in a persistent database

        :param location: The location in which to process
        :param mapset: The new mapset to generate
        :param process_chain: The process chain that must be executed
        :return: Status code and the json data (status, json)
        """

        url = "%(base)s/locations/%(location)s/mapsets/%(mapset)s/processing_async" % {"base": self.base_url,
                                                                                       "location": location,
                                                                                       "mapset": mapset}
        return self._send_post_request(url=url, process_chain=process_chain)

    def async_ephemeral_processing(self, location, process_chain):
        """Send a process chain to the Actinia backend to be run asynchronously in a ephemeral database

        :param location: The location in which to process
        :param process_chain: The process chain that must be executed
        :return: Status code and the json data (status, json)
        """

        url = "%(base)s/locations/%(location)s/processing_async" % {"base": self.base_url,
                                                                    "location": location}
        return self._send_post_request(url=url, process_chain=process_chain)

    def async_ephemeral_processing_export(self, location, process_chain):
        """Send a process chain to the Actinia backend to be run asynchronously in a ephemeral database
        with export capabilities

        :param location: The location in which to process
        :param process_chain: The process chain that must be executed
        :return: Status code and the json data (status, json)
        """

        url = "%(base)s/locations/%(location)s/processing_async_export_gcs" % {"base": self.base_url,
                                                                           "location": location}
        return self._send_post_request(url=url, process_chain=process_chain)
