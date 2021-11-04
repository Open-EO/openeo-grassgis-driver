# -*- coding: utf-8 -*-
import json

from openeo_grass_gis_driver.actinia_processing.base import \
     check_node_parents, DataObject, GrassDataType, \
     create_output_name
from openeo_grass_gis_driver.models.process_graph_schemas import \
     ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import \
     Parameter, ProcessDescription, ReturnValue, ProcessExample
from .base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

# dummy math processes


PROCESS_DESCRIPTION_DICT["cos"] = {
    "id": "cos",
    "summary": "Cosine",
    "description": "Computes the cosine of `x`.\n\nWorks on radians only.\nThe no-data value `null` is passed through and therefore gets propagated.",
    "categories": [
        "math > trigonometric"
    ],
    "parameters": [
        {
            "name": "x",
            "description": "An angle in radians.",
            "schema": {
                "type": [
                    "number",
                    "null"
                ]
            }
        }
    ],
    "returns": {
        "description": "The computed cosine of `x`.",
        "schema": {
            "type": [
                "number",
                "null"
            ]
        }
    },
    "examples": [
        {
            "arguments": {
                "x": 0
            },
            "returns": 1
        }
    ],
    "links": [
        {
            "rel": "about",
            "href": "http://mathworld.wolfram.com/Cosine.html",
            "title": "Cosine explained by Wolfram MathWorld"
        }
    ]
}


PROCESS_DESCRIPTION_DICT["sin"] = {
    "id": "sin",
    "summary": "Sine",
    "description": "Computes the sine of `x`.\n\nWorks on radians only.\nThe no-data value `null` is passed through and therefore gets propagated.",
    "categories": [
        "math > trigonometric"
    ],
    "parameters": [
        {
            "name": "x",
            "description": "An angle in radians.",
            "schema": {
                "type": [
                    "number",
                    "null"
                ]
            }
        }
    ],
    "returns": {
        "description": "The computed sine of `x`.",
        "schema": {
            "type": [
                "number",
                "null"
            ]
        }
    },
    "examples": [
        {
            "arguments": {
                "x": 0
            },
            "returns": 0
        }
    ],
    "links": [
        {
            "rel": "about",
            "href": "http://mathworld.wolfram.com/Sine.html",
            "title": "Sine explained by Wolfram MathWorld"
        }
    ]
}
