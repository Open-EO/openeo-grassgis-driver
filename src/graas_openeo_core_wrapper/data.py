# -*- coding: utf-8 -*-
from openeo_core.data import Data
from openeo_core.definitions import DataSetInfo
from graas_openeo_core_wrapper.graas_wrapper import GRaaSInterface
from flask import make_response, jsonify


class GRaaSData(Data):

    def __init__(self):
        self.iface = GRaaSInterface()

    def get(self, ):

        # # List raster maps from the GRASS location
        # status_code, raster_data = self.iface.list_raster()
        # if status_code != 200:
        #     return make_response(jsonify({"description":"An internal error occurred "
        #                                                 "while catching raster layers!"}, 400))
        #
        # # List vector maps from the GRASS location
        # status_code, vector_data = self.iface.list_raster()
        # if status_code != 200:
        #     return make_response(jsonify({"description":"An internal error occurred "
        #                                                 "while catching vector layers!"}, 400))

        # List strds maps from the GRASS location
        status_code, strds_data = self.iface.list_strds()
        if status_code != 200:
            return make_response(jsonify({"description":"An internal error occurred "
                                                        "while catching strds layers!"}, 400))

        dataset_list = []
        for entry in strds_data:
            ds = DataSetInfo(product_id=entry, description="Space time raster dataset",
                             source="%s/%s"%(self.iface.location, self.iface.mapset))
            dataset_list.append(ds)

        return make_response(jsonify(dataset_list), 200)
