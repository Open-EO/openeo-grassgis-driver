# -*- coding: utf-8 -*-
import json
from random import randint
from typing import List, Tuple

from openeo_grass_gis_driver.actinia_processing.base import check_node_parents
from openeo_grass_gis_driver.process_schemas import Parameter, ProcessDescription, ReturnValue
from .base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "filter_bbox"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)
    p_left = Parameter(description="The left (western) border of the spatial extent",
                       schema={"type": "object", "format": "float"},
                       required=True)
    p_right = Parameter(description="The right (eastern) border of the spatial extent",
                        schema={"type": "object", "format": "float"},
                        required=True)
    p_top = Parameter(description="The top (northern) border of the spatial extent",
                      schema={"type": "object", "format": "float"},
                      required=True)
    p_bottom = Parameter(description="The bottom (southern) border of the spatial extent",
                         schema={"type": "object", "format": "float"},
                         required=True)
    p_width_res = Parameter(description="The width resolution of the spatial extent",
                            schema={"type": "object", "format": "float"},
                            required=True)
    p_height_res = Parameter(description="The height resolution of the spatial extent",
                             schema={"type": "object", "format": "float"},
                             required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    examples = dict(simple={
        "filter_bbox_1": {
            "process_id": "filter_bbox",
            "arguments": {
                "data": {"from_node": "get_data_1"},
                "left": 630000,
                "right": 645000,
                "top": 228500,
                "bottom": 215000,
                "width_res": 10,
                "height_res": 10,
            }
        }
    })

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Drops observations from raster data or raster time series data "
                                        " that are located outside of a given bounding box.",
                            summary="Filter raster based data by bounding box",
                            parameters={"data": p_data,
                                        "left": p_left,
                                        "right": p_right,
                                        "top": p_top,
                                        "bottom": p_bottom,
                                        "width_res": p_width_res,
                                        "hieght_res": p_height_res},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(left: float, right: float, top: float,
                               bottom: float, width_res: float, height_res: float) -> dict:
    """Create a Actinia command of the process chain that uses g.region to create a valid computational region
    for the provide input strds

    :param left:
    :param right:
    :param top:
    :param bottom:
    :param width_res:
    :param height_res:
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    pc = {"id": "g_region_%i" % rn,
          "module": "g.region",
          "inputs": [{"param": "n", "value": str(top)},
                     {"param": "s", "value": str(bottom)},
                     {"param": "e", "value": str(right)},
                     {"param": "w", "value": str(left)},
                     {"param": "ewres", "value": str(width_res)},
                     {"param": "nsres", "value": str(height_res)}]}

    return pc


def get_process_list(node: Node) -> Tuple[list, list]:
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_names, actinia_process_list)
    """

    input_names, process_list = check_node_parents(node=node)
    output_names = []

    if "data" not in node.arguments or \
            "left" not in node.arguments or \
            "right" not in node.arguments or \
            "top" not in node.arguments or \
            "bottom" not in node.arguments or \
            "width_res" not in node.arguments or \
            "height_res" not in node.arguments:
        raise Exception("Process %s requires parameter data, left, right, top, bottom, "
                        "width_res, height_res" % PROCESS_NAME)

    left = node.arguments["left"]
    right = node.arguments["right"]
    top = node.arguments["top"]
    bottom = node.arguments["bottom"]
    width_res = node.arguments["width_res"]
    height_res = node.arguments["height_res"]

    pc = create_process_chain_entry(left=left, right=right, top=top,
                                    bottom=bottom, width_res=width_res,
                                    height_res=height_res)
    process_list.append(pc)

    for input_name in node.get_parent_by_name(parent_name="data").output_names:
        # Create the output name based on the input name and method
        output_name = input_name
        output_names.append(output_name)
        node.add_output(output_name)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
