# -*- coding: utf-8 -*-
from flask_restful import Resource
from flask import make_response, jsonify, request

from openeo_grass_gis_driver.actinia_processing.actinia_interface import \
     ActiniaInterface
from openeo_grass_gis_driver.actinia_processing.config import Config
from openeo_grass_gis_driver.models.collection_schemas import \
     Collection, CollectionEntry


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert, Carmen Tawalika"
__copyright__ = "Copyright 2018-2021, Sören Gebbert, mundialis"
__maintainer__ = "mundialis"


COLLECTIONS_LIST = []


class Collections(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()

    def get(self):

        global COLLECTIONS_LIST

        # if endpoint is called with GET parameter /collections?cache=false
        # then the cache is reloaded.
        if 'cache' in request.args and request.args['cache'] == "false":
            COLLECTIONS_LIST = []

        # when cache is reloaded or COLLECTIONS_LIST is empty on startup, fill.
        if not COLLECTIONS_LIST:

            for location in Config.LOCATIONS:

                status_code, mapsets = (self.iface.list_mapsets(
                    location=location))
                if status_code != 200:
                    return make_response(
                        jsonify(
                            {
                                "description": "An internal error occurred "
                                "while catching mapset "
                                "from location %s!" %
                                location}, 400))

                for mapset in mapsets:

                    # List strds maps from the GRASS location
                    status_code, strds_data = self.iface.list_strds(
                        location=location, mapset=mapset)
                    if status_code != 200:
                        return make_response(jsonify(
                            {"description": "An internal error occurred "
                             "while catching strds layers for mapset %s "
                             "in location %s !" % (mapset, location)}, 400))

                    for entry in strds_data:
                        strds_id = "%s.%s.strds.%s" % (location, mapset, entry)
                        ds = CollectionEntry(
                            id=strds_id,
                            title="Space time raster dataset",
                            license="proprietary",
                            description=("Space time raster dataset GRASS GIS "
                                         " location/mapset path: /%s/%s" % (
                                          location, mapset)))
                        COLLECTIONS_LIST.append(ds)

                    # # List vector maps from the GRASS location
                    # status_code, vector_data = self.iface.list_vector(
                    #     location=location, mapset=mapset)
                    # if status_code != 200:
                    #     return make_response(jsonify(
                    #         {"description": "An internal error occurred "
                    #          "while catching vector layers!"}, 400))

                    # for entry in vector_data:
                    #     vector_id = ("%s.%s.vector.%s" % (
                    #         location, mapset, entry))
                    #     ds = CollectionEntry(
                    #         id=vector_id,
                    #         title="Vector dataset",
                    #         license="proprietary",
                    #         description=("Raster Vector GRASS GIS location "
                    #                      "mapset path: /%s/%s" % (
                    #                       location, mapset)))
                    #     COLLECTIONS_LIST.append(ds)

            # Additionally check for STAC collections registered in actinia
            status_code, stac_collections = self.iface.get_stac_collections()
            if status_code != 200:
                stac_collections = []

            for i in stac_collections['collections']:
                try:
                    title = i['title']
                except Exception:
                    title = i['id']
                try:
                    license = i['license']
                except Exception:
                    license = "proprietary"
                try:
                    description = i['description']
                except Exception:
                    description = "STAC collection registered in actinia"

                ds = CollectionEntry(
                    id=i['id'],
                    title=title,
                    license=license,
                    description=description
                )
                COLLECTIONS_LIST.append(ds)

        c = Collection(collections=COLLECTIONS_LIST)
        return c.as_response(http_status=200)
