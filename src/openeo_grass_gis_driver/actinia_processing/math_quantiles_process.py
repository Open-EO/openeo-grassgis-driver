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
PROCESS_NAME = "quantiles"


def create_process_description():
    p_data = Parameter(description="An array of numbers.",
                       schema={
                               "type": "array",
                               "items": {
                                 "type": [
                                   "number",
                                   "null"
                                 ]
                               }
                       })
    p_prob = Parameter(
        description="A list of probabilities to calculate quantiles for. The probabilities must be between 0 and 1.",
        schema={
            "type": "array",
            "items": {
                "type": "number",
                "minimum": 0,
                "maximum": 1}},
        optional=True)
    p_quant = Parameter(
        description="A number of intervals to calculate quantiles for. Calculates q-quantiles with (nearly) equal-sized intervals.",
        schema={
            "type": "integer",
            "minimum": 2},
        optional=True)
    p_nodata = Parameter(
        description="Indicates whether no-data values are ignored or not.",
        schema={
            "type": "boolean"},
        default=True,
        optional=True)

    rv = ReturnValue(description="An array with the computed quantiles.",
                     schema={
                             "type": "array",
                             "items": {
                               "type": [
                                 "number",
                                 "null"
                               ]
                                 }
                     })

    # Example
    arguments = {
        "data": [
          2,
          4,
          4,
          4,
          5,
          5,
          7,
          9
        ],
        "probabilities": [
          0.005,
          0.01,
          0.02,
          0.05,
          0.1,
          0.5
        ]
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "quantiles_1": node})
    examples = [
        ProcessExample(
            title="Simple example",
            description="Simple example",
            process_graph=graph)]

    pd = ProcessDescription(
        id=PROCESS_NAME,
        description="Calculates quantiles, which are cut points dividing the range of a probability distribution.",
        summary="Quantiles",
        parameters={
            "data": p_data,
            "probabilities": p_prob,
            "q": p_quant,
            "ignore_nodata": p_nodata},
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
        name=create_output_name(input_object.name, PROCESS_NAME),
        datatype=GrassDataType.STRDS)
    output_objects.append(output_object)

    # pc = create_process_chain_entry(input_object, vector_object, output_object)
    # process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
