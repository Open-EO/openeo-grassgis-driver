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

PROCESS_NAME = "add_dimension"


def create_process_description():
    p_data = Parameter(description="A data cube to add the dimension to.",
                       schema={"type": "object", "subtype": "raster-cube"},
                       optional=False)
    p_name = Parameter(description="Name for the dimension.",
                       schema={"type": "string"})
    p_label = Parameter(description="A dimension label.",
                        schema=[
                                {
                                  "type": "number"
                                },
                                {
                                  "type": "string"
                                }
                              ])
    p_type = Parameter(description="The type of dimension, defaults to `other`.",
                       schema={
                                "type": "string",
                                "enum": [
                                  "spatial",
                                  "temporal",
                                  "bands",
                                  "other"
                                ]
                              },
                       default="other",
                       optional=True)

    rv = ReturnValue(description="The data cube with a newly added dimension. "
                                 "The new dimension has exactly one dimension label. "
                                 "All other dimensions remain unchanged.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "data": {"from_node": "get_data_1"},
        "name": "bands",
        "label": "spectral bands",
        "type": "spatial"
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"add_dimension_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Limits the data cube over the spatial dimensions to the specified polygons.\n\nThe filter retains "
                            "a pixel in the data cube if the point at the pixel center intersects with at least one of the polygons (as  "
                            "defined in the Simple Features standard by the OGC).",
                            summary="Spatial filter using polygons",
                            parameters={"data": p_data,
                                        "name": p_name,
                                        "label": p_label,
                                        "type": p_type},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object: DataObject,
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

    input_objects = node.get_parent_by_name(parent_name="data").output_objects

    if not input_objects:
        raise Exception("Process %s requires an input strds" % PROCESS_NAME)

    for data_object in input_objects:
        output_objects.append(data_object)
        node.add_output(data_object)

    # pc = create_process_chain_entry(input_object, output_object)
    # process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
