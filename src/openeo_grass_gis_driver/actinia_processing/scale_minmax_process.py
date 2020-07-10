# -*- coding: utf-8 -*-
import json
from random import randint
from typing import List, Tuple

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from .base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

from flask import make_response, jsonify, request

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

# not in the official list
PROCESS_NAME = "scale_minmax"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "subtype": "raster-cube"},
                       required=True)
    p_min = Parameter(description="New minimum value",
                      schema={"type": "object", "format": "float"},
                      required=True)
    p_max = Parameter(description="New maximum value",
                      schema={"type": "object", "format": "float"},
                      required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "data": {"from_node": "get_data_1"},
        "min": 1,
        "max": 255,
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"scale_minmax_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]
    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Scales the image values between specified min and max values.",
                            summary="Rescale raster data based on interval",
                            parameters={"data": p_data,
                                        "min": p_min,
                                        "max": p_max},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object, newmin, newmax, output_object):
    """Create a Actinia command of the process chain that uses t.rast.mapcalc 
    to rescale raster values to the specified interval

    :param input_object: The input openeo map name
    :param min: new minimum value
    :param max: new maximum value
    :param output_object: The output raster map name
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    pc = {"id": "r_scaleminmax_%i" % rn,
          "module": "r.scaleminmax",
          "inputs": [{"param": "input",
                      "value": input_object.grass_name()},
                     {"param": "output",
                      "value": output_object.grass_name()},
                     {"param": "min",
                      "value": newmin},
                     {"param": "max",
                      "value": newmax},
                    ]}

    return pc


def get_process_list(node: Node) -> Tuple[list, list]:
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "data" not in node.arguments or \
            "min" not in node.arguments or \
            "max" not in node.arguments:
        raise Exception("Process %s requires parameter data, min, max" % PROCESS_NAME)

    newmin = node.arguments["min"]
    newmax = node.arguments["max"]

    # for each raster separately
    for input_object in node.get_parent_by_name("data").output_objects:

        output_object = DataObject(name=f"{input_object.name}_{PROCESS_NAME}", datatype=GrassDataType.RASTER)
        output_objects.append(output_object)
        node.add_output(output_object=output_object)

        pc = create_process_chain_entry(input_object, newmin, newmax, output_object)
        process_list.append(pc)

    # TODO: create strds from output raster maps

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
