# -*- coding: utf-8 -*-
from .definitions import DataSetListEntry
from .actinia_processing.actinia_interface import ActiniaInterface
from flask import make_response, jsonify
from flask_restful import Resource
from .actinia_processing.config import Config

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

GET_DATA_EXAMPLE = [
    {
        "product_id": "MOD09Q1",
        "description": " MODIS/Terra Surface Reflectance 8-Day L3 Global 250m SIN Grid V006",
        "source": "U.S. Geological Survey (USGS), DOI: 10.5067/MODIS/MOD09Q1.006"
    },
    {
        "product_id": "SENTINEL2-1C",
        "description": "Sentinel 2 Level-1C: Top-of-atmosphere reflectances in cartographic geometry",
        "source": "European Space Agency (ESA)"
    },
    {
        "product_id": "LandsatETM+",
        "description": "Landsat Enhanced Thematic Mapper Plus (ETM+)",
        "source": "U.S. Geological Survey (USGS)"
    }
]

GET_DATA_DOC = {
    "summary": "Returns basic information about EO datasets that are available at the back-end and "
               "offers simple search by time, space, and product name.",
    "description": "Requests will ask the back-end for available data and will return an array of available datasets "
                   "with very basic information such as their unique identifiers. Results can be filtered by space, "
                   "time, and product name with very simple search expressions.",
    "tags": ["EO Data Discovery"],
    "parameters": [
        {
            "in": "query",
            "name": "qname",
            "type": "string",
            "description": "string expression to search available datasets by name",
            "required": False
        },
        {
            "in": "query",
            "name": "qgeom",
            "type": "string",
            "description": "WKT polygon to search for available datasets that spatially intersect with the polygon",
            "required": False
        },
        {
            "in": "query",
            "name": "qstartdate",
            "type": "string",
            "description": "ISO 8601 date/time string to find datasets with any data acquired after the given date/time",
            "required": False
        },
        {
            "in": "query",
            "name": "qenddate",
            "type": "string",
            "description": "ISO 8601 date/time string to find datasets with any data acquired before the given date/time",
            "required": False
        }
    ],
    "responses": {
        "200": {
            "description": "An array of EO datasets including their unique identifiers and some basic metadata.",
            "schema": {"type": "array",
                       "items": DataSetListEntry
                       },
            "examples": {"application/json": GET_DATA_EXAMPLE}
        },
        "401": {"$ref": "#/responses/auth_required"},
        "501": {"$ref": "#/responses/not_implemented"},
        "503": {"$ref": "#/responses/unavailable"}
    }
}

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
