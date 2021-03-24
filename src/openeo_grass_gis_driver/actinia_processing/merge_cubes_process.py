# -*- coding: utf-8 -*-
import json
from random import randint
from typing import List, Tuple

from openeo_grass_gis_driver.actinia_processing.base import check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from .base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "merge_cubes"


def create_process_description():
    p_data1 = Parameter(description="Any openEO process object that returns raster datasets "
                        "or space-time raster dataset",
                        schema={"type": "object", "subtype": "raster-cube"},
                        optional=False)
    p_data2 = Parameter(description="Any openEO process object that returns raster datasets "
                        "or space-time raster dataset",
                        schema={"type": "object", "subtype": "raster-cube"},
                        optional=False)
    # the overlap_resolver is not supported by us
    p_resolver = Parameter(description="A reduction operator that resolves the conflict if the data overlaps",
                           schema={"type": "object",
                                   "subtype": "process-graph",
                                   "parameters": [{
                                    "name": "x",
                                    "description": "The first value.",
                                    "schema": {
                                      "description": "Any data type."
                                    }
                                    },
                                    {
                                    "name": "y",
                                    "description": "The second value.",
                                    "schema": {
                                      "description": "Any data type."
                                    }
                                    },
                                    {
                                    "name": "context",
                                    "description": "Additional data passed by the user.",
                                    "schema": {
                                      "description": "Any data type."
                                    },
                                    "required": False,
                                    "default": "null"
                                    }
                                    ]
                                   },
                           optional=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "cube1": {"from_node": "get_data_1"},
        "cube2": {"from_node": "get_data_2"},
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"merge_cubes_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="The data cubes have to be compatible. A merge is the inverse of a split if there is no overlap.",
                            summary="Merging two data cubes",
                            parameters={"cube1": p_data1,
                                        "cube2": p_data2,
                                        "overlap_resolver": p_resolver},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(cube1_object: DataObject, cube2_object: DataObject,
                               output_object: DataObject):
    """Create a Actinia command of the process chain

    :param cube1_object:
    :param cube2_object:
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    # t.merge does not have a method to resolve overlaps

    pc = {"id": "t_merge_%i" % rn,
          "module": "t.merge",
          "inputs": [{"param": "inputs",
                     "value": "%(cube1)s,%(cube2)s" % {"cube1": cube1_object.grass_name(), "cube2": cube2_object.grass_name()}},
                     {"param": "output",
                     "value": output_object.grass_name()}]}

    return pc


def get_process_list(node: Node):
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "cube1" not in node.arguments or \
            "cube2" not in node.arguments:
        raise Exception("Process %s requires parameter cube1, cube2" % PROCESS_NAME)

    cube1_objects = node.get_parent_by_name(parent_name="cube1").output_objects
    cube2_objects = node.get_parent_by_name(parent_name="cube2").output_objects

    if "overlap_resolver" in node.arguments and \
        (node.arguments["overlap_resolver"] is not None or
            node.arguments["overlap_resolver"] != "null"):
        raise Exception("Process %s does not support yet the parameter \"overlap_resolver\"" % PROCESS_NAME)

    if not cube1_objects:
        raise Exception("Process %s requires two input strds's" % PROCESS_NAME)

    if not cube2_objects:
        raise Exception("Process %s requires two input strds's" % PROCESS_NAME)

    cube1_object = list(cube1_objects)[-1]
    cube2_object = list(cube2_objects)[-1]

    output_object = DataObject(name=f"{cube1_object.name}_{PROCESS_NAME}", datatype=GrassDataType.STRDS)
    output_objects.append(output_object)
    node.add_output(output_object=output_object)

    pc = create_process_chain_entry(cube1_object, cube2_object, output_object)
    process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
