# -*- coding: utf-8 -*-
from openeo_core.data import Data, GET_DATA_DOC
from openeo_core.definitions import DataSetListEntry, DataSetInfo
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from flask import make_response, jsonify
from flask_restful_swagger_2 import swagger
from graas_openeo_core_wrapper.config import Config


class GRaaSData(Data):

    def __init__(self):
        self.iface = GRaaSInterface()

    @swagger.doc(GET_DATA_DOC)
    def get(self, ):

        dataset_list = []

        for location in Config.LOCATIONS:

            status_code, mapsets = self.iface.list_mapsets(location=location)
            if status_code != 200:
                return make_response(jsonify({"description":"An internal error occurred "
                                                            "while catching mapset "
                                                            "from location %s!"%location}, 400))

            for mapset in mapsets:

                # List strds maps from the GRASS location
                status_code, strds_data = self.iface.list_strds(location=location, mapset=mapset)
                if status_code != 200:
                    return make_response(jsonify({"description":"An internal error occurred "
                                                                "while catching strds layers!"}, 400))

                for entry in strds_data:
                    strds_id = "%s.%s.strds.%s"%(location, mapset, entry)
                    ds = DataSetListEntry(product_id=strds_id, description="Space time raster dataset",
                                          source="GRASS GIS location/mapset path: "
                                                 "/%s/%s"%(location, mapset))
                    dataset_list.append(ds)

                # List raster maps from the GRASS location
                status_code, raster_data = self.iface.list_raster(location=location, mapset=mapset)
                if status_code != 200:
                    return make_response(jsonify({"description":"An internal error occurred "
                                                                "while catching strds layers!"}, 400))

                for entry in raster_data:
                    raster_id = "%s.%s.raster.%s"%(location, mapset, entry)
                    ds = DataSetListEntry(product_id=raster_id, description="Raster dataset",
                                          source="GRASS GIS location/mapset path: "
                                                 "/%s/%s"%(location, mapset))
                    dataset_list.append(ds)

        return make_response(jsonify(dataset_list), 200)
