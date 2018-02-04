# -*- coding: utf-8 -*-
from openeo_core.data import Data, GET_DATA_DOC
from openeo_core.definitions import DataSetListEntry, DataSetInfo
from graas_openeo_core_wrapper.graas_wrapper import GRaaSInterface
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger


class GRaaSData(Data):

    def __init__(self):
        self.iface = GRaaSInterface()

    @swagger.doc(GET_DATA_DOC)
    def get(self, ):

        # List strds maps from the GRASS location
        status_code, strds_data = self.iface.list_strds()
        if status_code != 200:
            return make_response(jsonify({"description":"An internal error occurred "
                                                        "while catching strds layers!"}, 400))

        dataset_list = []
        for entry in strds_data:
            ds = DataSetListEntry(product_id=entry, description="Space time raster dataset",
                                  source="GRASS GIS location/mapset path: "
                                         "/%s/%s"%(self.iface.location, self.iface.mapset))
            dataset_list.append(ds)

        return make_response(jsonify(dataset_list), 200)
