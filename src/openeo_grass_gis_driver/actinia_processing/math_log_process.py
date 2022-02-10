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

# dummy math process
PROCESS_NAME = "log"


def create_process_description():
    p_x = Parameter(description="A number to compute the logarithm for.",
                    schema={
                               "type": [
                                 "number",
                                 "null"
                               ]
                       })
    p_y = Parameter(description="The numerical base.",
                    schema={
                               "type": [
                                 "number",
                                 "null"
                               ]
                       })

    rv = ReturnValue(description="The computed logarithm.",
                     schema={
                             "type": [
                               "number",
                               "null"
                             ],
                     })

    # Example
    arguments = {
        "x": 10,
        "base": 10
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "log_1": node})
    examples = [
        ProcessExample(
            title="Simple example",
            description="Simple example",
            process_graph=graph)]

    pd = ProcessDescription(
        id=PROCESS_NAME,
        description="Logarithm to the base `base` of the number `x` is defined to be the inverse function of taking b to the power of x.",
        summary="Logarithm to a base",
        parameters={
            "x": p_x,
            "base": p_y},
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

    output_object = DataObject(
        name=create_output_name(input_object.name, node),
        datatype=GrassDataType.STRDS)
    output_objects.append(output_object)

    # pc = create_process_chain_entry(input_object, vector_object, output_object)
    # process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
