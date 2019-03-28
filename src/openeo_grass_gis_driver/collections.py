# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import make_response, jsonify, request

from .actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.actinia_processing.config import Config
from openeo_grass_gis_driver.collection_schemas import Collection, CollectionEntry

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class Collections(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()

    def get(self):

        dataset_list = []

        for location in Config.LOCATIONS:

            status_code, mapsets = self.iface.list_mapsets(location=location)
            if status_code != 200:
                return make_response(jsonify({"description": "An internal error occurred "
                                                             "while catching mapset "
                                                             "from location %s!" % location}, 400))

            for mapset in mapsets:

                # List strds maps from the GRASS location
                status_code, strds_data = self.iface.list_strds(location=location, mapset=mapset)
                if status_code != 200:
                    return make_response(jsonify({"description": "An internal error occurred "
                                                                 "while catching strds layers!"}, 400))

                for entry in strds_data:
                    strds_id = "%s.%s.strds.%s" % (location, mapset, entry)
                    ds = CollectionEntry(name=strds_id,
                                         title="Space time raster dataset",
                                         license="unknown",
                                         description="Space time raster dataset GRASS GIS location/mapset path: /%s/%s" % (location, mapset))
                    dataset_list.append(ds)

                # List raster maps from the GRASS location
                status_code, raster_data = self.iface.list_raster(location=location, mapset=mapset)
                if status_code != 200:
                    return make_response(jsonify({"description": "An internal error occurred "
                                                                 "while catching raster layers!"}, 400))

                for entry in raster_data:
                    raster_id = "%s.%s.raster.%s" % (location, mapset, entry)
                    ds = CollectionEntry(name=raster_id,
                                         title="Raster dataset",
                                         license="unknown",
                                         description="Raster dataset GRASS GIS location/mapset path: /%s/%s" % (location, mapset))
                    dataset_list.append(ds)

                # List vector maps from the GRASS location
                status_code, vector_data = self.iface.list_vector(location=location, mapset=mapset)
                if status_code != 200:
                    return make_response(jsonify({"description": "An internal error occurred "
                                                                 "while catching vector layers!"}, 400))

                for entry in vector_data:
                    vector_id = "%s.%s.vector.%s" % (location, mapset, entry)
                    ds = CollectionEntry(name=vector_id,
                                         title="Vector dataset",
                                         license="unknown",
                                         description="Raster Vector GRASS GIS location/mapset path: /%s/%s" % (
                                         location, mapset))
                    dataset_list.append(ds)

        c = Collection(collections=dataset_list)

        return make_response(c.to_json(), 200)
