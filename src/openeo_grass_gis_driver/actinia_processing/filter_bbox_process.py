# -*- coding: utf-8 -*-
import json
from random import randint
from typing import List, Tuple

from openeo_grass_gis_driver.actinia_processing.base import check_node_parents
from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from .base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "filter_bbox"

# does not conform to
# https://open-eo.github.io/openeo-api/v/0.4.2/processreference/#filter_bbox

def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "subtype": "raster-cube"},
                       required=True)
    p_extent = Parameter(description="A bounding box, which may include a vertical axis (see `base` and `height`).\n\nThe coordinate reference system of the extent must be specified as [EPSG](http://www.epsg.org) code or [PROJ](https://proj4.org) definition.",
                       schema={
                                "type": "object",
                                "subtype": "bounding-box",
                                "required": [
                                  "west",
                                  "south",
                                  "east",
                                  "north"
                                ],
                                "properties": {
                                  "west": {
                                    "description": "West (lower left corner, coordinate axis 1).",
                                    "type": "number"
                                  },
                                  "south": {
                                    "description": "South (lower left corner, coordinate axis 2).",
                                    "type": "number"
                                  },
                                  "east": {
                                    "description": "East (upper right corner, coordinate axis 1).",
                                    "type": "number"
                                  },
                                  "north": {
                                    "description": "North (upper right corner, coordinate axis 2).",
                                    "type": "number"
                                  },
                                  "base": {
                                    "description": "Base (optional, lower left corner, coordinate axis 3).",
                                    "type": [
                                      "number",
                                      "null"
                                    ],
                                    "default": "null"
                                  },
                                  "height": {
                                    "description": "Height (optional, upper right corner, coordinate axis 3).",
                                    "type": [
                                      "number",
                                      "null"
                                    ],
                                    "default": "null"
                                  },
                                  "crs": {
                                    "description": "Coordinate reference system of the extent, specified as as [EPSG code](http://www.epsg-registry.org/), [WKT2 (ISO 19162) string](http://docs.opengeospatial.org/is/18-010r7/18-010r7.html) or [PROJ definition (deprecated)](https://proj.org/usage/quickstart.html). Defaults to `4326` (EPSG code 4326) unless the client explicitly requests a different coordinate reference system.",
                                    "schema": {
                                      "anyOf": [
                                        {
                                          "title": "EPSG Code",
                                          "type": "integer",
                                          "subtype": "epsg-code",
                                          "examples": [
                                            7099
                                          ]
                                        },
                                        {
					  "title": "WKT2",
					  "type": "string",
					  "subtype": "wkt2-definition"
                                        },
				        {
					  "title": "PROJ definition",
					  "type": "string",
					  "subtype": "proj-definition",
					  "deprecated": true
				        }
                                      ],
                                      "default": 4326
                                    }
                                  }
                                }
                            },
                    required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
                "data": {"from_node": "get_data_1"},
                "extent": {
                    "north": 51.00226308446294,
                    "crs": "EPSG:4326",
                    "west": 3.057030657924054,
                    "east": 3.058236553549667,
                    "south": 50.99958367677388
                },
            }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"filter_bbox_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Spatial filter using a bounding box",
                            summary="Spatial filter using a bounding box",
                            parameters={"data": p_data,
                                        "extent": p_extent},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(north: float, south: float, east: float,
                               west: float, crs: str) -> dict:
    """Create a Actinia command of the process chain that uses g.region to create a valid computational region
    for the provide input strds

    :param north:
    :param south:
    :param east:
    :param west:
    :param crs:
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    pc = {"id": "g_region_bbox_%i" % rn,
          "module": "g.region.bbox",
          "inputs": [{"param": "n", "value": str(north)},
                     {"param": "s", "value": str(south)},
                     {"param": "e", "value": str(east)},
                     {"param": "w", "value": str(west)},
                     {"param": "crs", "value": str(crs)},]}

    return pc


def get_process_list(node: Node) -> Tuple[list, list]:
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "data" not in node.arguments or \
            "extent" not in node.arguments or \
            "north" not in node.arguments["extent"] or \
            "south" not in node.arguments["extent"] or \
            "east" not in node.arguments["extent"] or \
            "west" not in node.arguments["extent"] or \
            "crs" not in node.arguments["extent"]:
        raise Exception("Process %s requires parameter data and extent with north, south, east, west, "
                        "crs" % PROCESS_NAME)

    north = node.arguments["extent"]["north"]
    south = node.arguments["extent"]["south"]
    west = node.arguments["extent"]["west"]
    east = node.arguments["extent"]["east"]
    if "crs" in node.arguments["extent"]:
        crs = node.arguments["extent"]["crs"]
    else:
        crs = "4326"

    if crs.isnumeric():
        crs = "EPSG:" + crs

    pc = create_process_chain_entry(north=north, south=south, east=east,
                                    west=west, crs=crs)
    process_list.append(pc)

    for data_object in node.get_parent_by_name(parent_name="data").output_objects:
        output_objects.append(data_object)
        node.add_output(data_object)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
