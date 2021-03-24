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

PROCESS_NAME = "array_element"


def create_process_description():
    p_data = Parameter(description="An array",
                       schema={
                                "type": "array",
                                "items": {
                                  "description": "Any data type is allowed."
                                }})
    p_index = Parameter(description="The zero-based index of the element to retrieve.",
                        schema={
                                "type": "integer"
                              },
                        optional=True)
    p_label = Parameter(description="The label of the element to retrieve.",
                       schema=[
                                {
                                  "type": "number"
                                },
                                {
                                  "type": "string"
                                }
                              ],
                        optional=True)

    rv = ReturnValue(description="The value of the requested element.",
                     schema={
                             "description": "Any data type is allowed."})

    # Example
    arguments = {
        "data": {"from_node": "get_data_1"},
        "index": 0,
        "label": 0
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"array_element_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Returns the element with the specified index or label from the array.",
                            summary="Get an element from an array",
                            parameters={"data": p_data,
                                        "index": p_index,
                                        "label": p_label},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object: DataObject, vector_object,
                               output_object: DataObject):
    """Create a Actinia command of the process chain

    :param input_object:
    :return: A Actinia process chain description
    """

    # rn = randint(0, 1000000)

    pc = []

    return pc


def get_process_list(node: Node):
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "data" not in node.arguments:
        raise Exception("Process %s requires parameter data" % PROCESS_NAME)

    input_objects = node.get_parent_by_name(parent_name="data").output_objects

    if not input_objects:
        raise Exception("Process %s requires an input strds" % PROCESS_NAME)

    input_object = list(input_objects)[-1]

    output_object = DataObject(name=f"{input_object.name}_{PROCESS_NAME}", datatype=GrassDataType.STRDS)
    output_objects.append(output_object)

    # pc = create_process_chain_entry(input_object, vector_object, output_object)
    # process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
