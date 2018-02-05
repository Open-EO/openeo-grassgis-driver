# -*- coding: utf-8 -*-
from openeo_core.data import Data, GET_DATA_DOC
from openeo_core.definitions import DataSetListEntry, DataSetInfo
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger


class GRaaSData(Data):

    def __init__(self):
        self.iface = GRaaSInterface()

    @swagger.doc(GET_DATA_DOC)
    def get(self, ):

        dataset_list = []

        status_code, mapsets = self.iface.list_mapsets()
        if status_code != 200:
            return make_response(jsonify({"description":"An internal error occurred "
                                                        "while catching mapsets!"}, 400))

        for mapset in mapsets:
            # List strds maps from the GRASS location
            status_code, strds_data = self.iface.list_strds(mapset=mapset)
            if status_code != 200:
                return make_response(jsonify({"description":"An internal error occurred "
                                                            "while catching strds layers!"}, 400))

            for entry in strds_data:
                strds_id = "%s@%s"%(entry, mapset)
                ds = DataSetListEntry(product_id=strds_id, description="Space time raster dataset",
                                      source="GRASS GIS location/mapset path: "
                                             "/%s/%s"%(self.iface.location, mapset))
                dataset_list.append(ds)

        return make_response(jsonify(dataset_list), 200)
