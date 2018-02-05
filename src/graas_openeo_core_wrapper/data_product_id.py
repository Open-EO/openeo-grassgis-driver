# -*- coding: utf-8 -*-
from openeo_core.data_product_id import DataProductId, GET_DATA_PRODUCT_ID_DOC
from openeo_core.definitions import SpatialExtent, DateTime, BandDescription
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger


class GRaaSDataProductId(DataProductId):

    def __init__(self):
        self.iface = GRaaSInterface()

    @swagger.doc(GET_DATA_PRODUCT_ID_DOC)
    def get(self, product_id):

        # List strds maps from the GRASS location

        mapset = "PERMANENT"
        if "@" in product_id:
            product_id, mapset = product_id.split("@", 1)

        status_code, strds_data = self.iface.strds_info(mapset=mapset, strds_name=product_id)
        if status_code != 200:
            return make_response(jsonify({"description": "An internal error occurred "
                                                         "while catching strds layers!"}, 400))

        # Get the projection from the GRASS mapset
        status_code, mapset_info = self.iface.mapset_info(mapset=mapset)
        if status_code != 200:
            return make_response(jsonify({"description": "An internal error occurred "
                                                         "while catching mapset info!"}, 400))

        description = "Space time raster dataset"
        source = "GRASS GIS location/mapset path: /%s/%s" % (self.iface.location, mapset)
        srs = mapset_info["projection"]
        extent = SpatialExtent(left=float(strds_data["west"]),
                               right=float(strds_data["east"]),
                               top=float(strds_data["north"]),
                               bottom=float(strds_data["south"]),
                               srs=srs)

        time = DateTime()
        time["from"] = strds_data["start_time"]
        time["to"] = strds_data["end_time"]

        bands = BandDescription(band_id=strds_data["id"])

        info = dict(product_id=strds_data["id"],
                    extent=extent,
                    source=source,
                    description=description,
                    time=time,
                    bands=bands,
                    temporal_type=strds_data["start_time"],
                    number_of_maps=strds_data["number_of_maps"],
                    min_min=strds_data["min_min"],
                    min_max=strds_data["min_max"],
                    max_min=strds_data["max_min"],
                    max_max=strds_data["max_max"],
                    map_time=strds_data["map_time"],
                    granularity=strds_data["granularity"],
                    aggregation_type=strds_data["aggregation_type"],
                    creation_time=strds_data["creation_time"],
                    modification_time=strds_data["modification_time"],
                    mapset=strds_data["mapset"])

        return make_response(jsonify(info), 200)
