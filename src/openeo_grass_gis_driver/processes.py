# -*- coding: utf-8 -*-
from flask import make_response, jsonify
from flask_restful import Resource
from .actinia_processing.base import PROCESS_DESCRIPTION_DICT
from .definitions import ProcessListEntry

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

GET_PROCESSES_EXAMPLE = [
    {
        "name": "get_data",
        "summary": "Selects a dataset.",
        "description": "Filters and selects a single dataset provided by the back-end. "
                       "The back-end provider decides which of the potential datasets is "
                       "the most relevant one to be selected.",
        "min_parameters": 1,
        "parameters":
            {
                "data_id":
                    {
                        "description": "Filter by data id",
                        "schema":
                            {
                                "type": "string",
                                "examples": ["Sentinel2A-L1C"]
                            }

                    },
                "extent":
                    {
                        "description": "Filter by extent",
                        "schema":
                            {
                                "type": "object",
                                "required":
                                    ["left", "right", "top", "bottom"],
                                "properties":
                                    {
                                        "crs":
                                            {

                                                "description": "Coordinate reference system. EPSG codes must be supported. "
                                                               "In addition, proj4 strings should be supported by back-ends. "
                                                               "Whenever possible, it is recommended to use EPSG codes instead of "
                                                               "proj4 strings. Defaults to `EPSG:4326` unless the client explicitly "
                                                               "requests a different coordinate reference system.",
                                                "type": "string",
                                                "default": "EPSG:4326"

                                            },
                                        "left": {"type": "number"},
                                        "right":
                                            {"type": "number"},
                                        "top":
                                            {"type": "number"},
                                        "bottom":
                                            {"type": "number"}
                                    }
                            }

                    },
                "time":
                    {

                        "description": "Filter by time",
                        "schema":

                            {
                                "type": "string"
                            }

                    },
                "bands":
                    {

                        "description": "Filter by band IDs",
                        "schema":

                            {

                                "type": "array",
                                "items":

                                    {
                                        "type": "string"
                                    }
                            }

                    },
                "derived_from":
                    {

                        "description": "Filter by derived data set",
                        "schema":

                            {

                                "type":

                                    [
                                        "string",
                                        "null"
                                    ]
                            }

                    },
                "license":
                    {

                        "description": "Filter by license",
                        "schema":

                            {

                                "type": "string",
                                "examples":

                                    [
                                        "Apache-2.0"
                                    ],
                                "description": "If available, should be a license from the SPDX License List: https://spdx.org/licenses/"
                            }
                    }

            },
        "returns":
            {

                "description": "Processed EO data.",
                "schema":

                    {
                        "type": "object",
                        "format": "eodata"
                    }
            }
    },
    {
        "name": "filter_bands",
        "summary": "Filter an image collection by bands.",
        "description": "Allows to extract one or multiple bands of multi-band raster image collection.    Bands can be chosen either by band id, band name or by wavelength.    imagery and at least one of the other arguments is required to be specified.",
        "min_parameters": 2,
        "parameters":
            {

                "imagery":

                    {

                        "description": "EO data to process.",
                        "required": True,
                        "schema":

                            {
                                "type": "object",
                                "format": "eodata"
                            }

                    },
                "bands":
                    {
                        "description": "string or array of strings containing band ids.",
                        "schema":
                            {
                                "type":
                                    ["string","array"],
                                "items":{"type": "string"}
                            }
                    },
                "names":
                    {
                        "description": "string or array of strings containing band names.",
                        "schema":
                            {
                                "type":
                                    [

                                        "string",
                                        "array"

                                    ],
                                "items":

                                    {
                                        "type": "string"
                                    }
                            }

                    },
                "wavelengths":
                    {

                        "description": "number or two-element array of numbers containing a wavelength or a minimum and maximum wavelength respectively.",
                        "schema":

                            {

                                "type":

                                    [

                                        "number",
                                        "array"

                                    ],
                                "minItems": 2,
                                "maxItems": 2,
                                "items":

                                    {
                                        "type": "number"
                                    }
                            }
                    }

            },
        "returns":
            {

                "description": "Processed EO data.",
                "schema":

                    {
                        "type": "object",
                        "format": "eodata"
                    }
            }

    },
    {

        "name": "filter_daterange",
        "summary": "Filter an image collection by temporal extent.",
        "min_parameters": 1,
        "parameters":

            {

                "imagery":

                    {

                        "description": "EO data to process.",
                        "required": True,
                        "schema":

                            {
                                "type": "object",
                                "format": "eodata"
                            }

                    },
                "extent":
                    {

                        "type": "array",
                        "description": "Temporal extent specified by a start and an end time, each formatted as a [RFC 3339](https://www.ietf.org/rfc/rfc3339) date-time. Open date ranges are supported and can be specified by setting one of the times to null. Setting both entries to null is not allowed.",
                        "example":

                            [

                                "2016-01-01T00:00:00Z",
                                "2017-10-01T00:00:00Z"

                            ],
                        "items":
                            {

                                "type":

                                    [
                                        "string",
                                        "null"
                                    ],
                                "format": "date-time",
                                "minItems": 2,
                                "maxItems": 2
                            }
                    }

            },
        "returns":
            {

                "description": "Processed EO data.",
                "schema":

                    {
                        "type": "object",
                        "format": "eodata"
                    }
            }

    },
    {

        "name": "process_graph",
        "description": "Loads another process graph and applies it to the specified imagery. This can be an externally hosted process graph.",
        "parameters":

            {

                "imagery":

                    {

                        "description": "EO data to process.",
                        "required": True,
                        "schema":

                            {
                                "type": "object",
                                "format": "eodata"
                            }

                    },
                "url":
                    {

                        "description": "An URL to a process graph.",
                        "required": True,
                        "schema":

                            {

                                "type": "string",
                                "format": "url",
                                "examples":

                                    [
                                        "http://otherhost.org/api/v1/users/12345/process_graphs/abcdef"
                                    ]
                            }
                    }

            },
        "returns":
            {

                "description": "Processed EO data.",
                "schema":

                    {
                        "type": "object",
                        "format": "eodata"
                    }

            },
        "exceptions":
            {

                "NotFound":

                    {
                        "code": 404,
                        "description": "Process graph doesn't exist."
                    }
            }
    }

]

GET_PROCESSES_DOC = {
    "summary": "Returns processes supported by the back-end",
    "description": "The request will ask the back-end for available processes and will return an array "
                   "of available processes with their unique identifiers and description",
    "tags": ["Process Discovery"],
    "parameters": [
        {
            "name": "qname",
            "in": "query",
            "type": "string",
            "description": "string expression to search for available processes by name",
            "required": False
        }
    ],
    "responses": {
        "200": {
            "description": "An array of EO processes including their unique identifiers and a description.",
            "schema": {
                "type": "array",
                "items": ProcessListEntry
            },
            "examples": GET_PROCESSES_EXAMPLE
        },
        "401": {"$ref": "#/responses/auth_required"},
        "501": {"$ref": "#/responses/not_implemented"},
        "503": {"$ref": "#/responses/unavailable"}
    }
}


class Processes(Resource):

    def get(self):
        return make_response(jsonify(list(PROCESS_DESCRIPTION_DICT.keys())), 200)