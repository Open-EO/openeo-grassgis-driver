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

        location, mapset, datatype, layer = self.iface.layer_def_to_components(product_id)

        status_code, layer_data = self.iface.layer_info(layer_name=product_id)
        if status_code != 200:
            return make_response(jsonify({"description": "An internal error occurred "
                                                         "while catching GRASS GIS layer information "
                                                         "for layer <%s>!\n Error: %s"
                                                         ""%(product_id, str(layer_data))}, 400))

        # Get the projection from the GRASS mapset
        status_code, mapset_info = self.iface.mapset_info(location=location, mapset=mapset)
        if status_code != 200:
            return make_response(jsonify({"description": "An internal error occurred "
                                                         "while catching mapset info "
                                                         "for mapset <%s>!"%mapset}, 400))

        description = "Raster dataset"
        if datatype.lower() == "strds":
            description = "Space time raster dataset"
        if datatype.lower() == "vector":
            description = "Vector dataset"

        source = "GRASS GIS location/mapset path: /%s/%s" % (location, mapset)
        srs = mapset_info["projection"]
        extent = SpatialExtent(left=float(layer_data["west"]),
                               right=float(layer_data["east"]),
                               top=float(layer_data["north"]),
                               bottom=float(layer_data["south"]),
                               srs=srs)

        print(layer_data)

        if datatype.lower() == "strds":
            time = DateTime()
            time["from"] = layer_data["start_time"]
            time["to"] = layer_data["end_time"]

            bands = BandDescription(band_id=product_id)

            info = dict(product_id=product_id,
                        extent=extent,
                        source=source,
                        description=description,
                        time=time,
                        bands=bands,
                        temporal_type=layer_data["start_time"],
                        number_of_maps=layer_data["number_of_maps"],
                        min_min=layer_data["min_min"],
                        min_max=layer_data["min_max"],
                        max_min=layer_data["max_min"],
                        max_max=layer_data["max_max"],
                        map_time=layer_data["map_time"],
                        granularity=layer_data["granularity"],
                        aggregation_type=layer_data["aggregation_type"],
                        creation_time=layer_data["creation_time"],
                        modification_time=layer_data["modification_time"],
                        mapset=mapset,
                        location=location)
        else:
            info = dict(product_id=product_id,
                        extent=extent,
                        source=source,
                        description=description,
                        mapset=mapset,
                        location=location)

        return make_response(jsonify(info), 200)
