# -*- coding: utf-8 -*-
from .definitions import DataSetListEntry
from .actinia_processing.actinia_interface import ActiniaInterface
from flask import make_response, jsonify
from flask_restful import Resource
from .actinia_processing.config import Config

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

GET_DATA_EXAMPLE = [
  {
    "data_id": "MOD09Q1",
    "description": " MODIS/Terra Surface Reflectance 8-Day L3 Global 250m SIN Grid V006",
    "source": "U.S. Geological Survey (USGS), DOI: 10.5067/MODIS/MOD09Q1.006"
  },
  {
    "data_id": "SENTINEL2-1C",
    "description": "Sentinel 2 Level-1C: Top-of-atmosphere reflectances in cartographic geometry",
    "source": "European Space Agency (ESA)"
  },
  {
    "data_id": "LandsatETMPlus",
    "description": "Landsat Enhanced Thematic Mapper Plus (ETM+)",
    "source": "U.S. Geological Survey (USGS)"
  }
]

class Data(Resource):

    def __init__(self):
        self.iface = ActiniaInterface()

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
                    ds = DataSetListEntry(data_id=strds_id, description="Space time raster dataset",
                                          source="GRASS GIS location/mapset path: "
                                                 "/%s/%s"%(location, mapset))
                    dataset_list.append(ds)

                # List raster maps from the GRASS location
                status_code, raster_data = self.iface.list_raster(location=location, mapset=mapset)
                if status_code != 200:
                    return make_response(jsonify({"description":"An internal error occurred "
                                                                "while catching raster layers!"}, 400))

                for entry in raster_data:
                    raster_id = "%s.%s.raster.%s"%(location, mapset, entry)
                    ds = DataSetListEntry(data_id=raster_id, description="Raster dataset",
                                          source="GRASS GIS location/mapset path: "
                                                 "/%s/%s"%(location, mapset))
                    dataset_list.append(ds)

                # List vector maps from the GRASS location
                status_code, vector_data = self.iface.list_vector(location=location, mapset=mapset)
                if status_code != 200:
                    return make_response(jsonify({"description":"An internal error occurred "
                                                                "while catching vector layers!"}, 400))

                for entry in vector_data:
                    raster_id = "%s.%s.vector.%s"%(location, mapset, entry)
                    ds = DataSetListEntry(data_id=raster_id, description="Vector dataset",
                                          source="GRASS GIS location/mapset path: "
                                                 "/%s/%s"%(location, mapset))
                    dataset_list.append(ds)

        return make_response(jsonify(dataset_list), 200)
