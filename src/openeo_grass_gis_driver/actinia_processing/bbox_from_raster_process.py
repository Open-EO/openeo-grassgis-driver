# -*- coding: utf-8 -*-
import json
from random import randint
from typing import List, Tuple

from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface
from openeo_grass_gis_driver.actinia_processing.base import check_node_parents, DataObject
from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

# not in the official list
PROCESS_NAME = "bbox_from_raster"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets",
                       schema={"type": "object", "subtype": "raster-cube"},
                       optional=False)
    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "data": {"from_node": "get_data_1"},
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"bbox_from_raster_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Sets the computational bounding box for "
                                        "downstream computation from raster layer.",
                            summary="Sets the computational bounding box for "
                                        "downstream computation from raster layer.",
                            parameters={"data": p_data},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(data_object: DataObject) -> dict:
    """Create a Actinia command of the process chain that uses g.region to create a valid computational region
    for the provide input strds

    :param data_object: Input raster map data object
    :return: A Actinia process chain description
    """
    rn = randint(0, 1000000)

    pc = {"id": "g_region_%i" % rn,
          "module": "g.region",
          "inputs": [{"param": "raster", "value": str(data_object.grass_name())}],
          "flags": "p"}

    return pc


def get_process_list(node: Node) -> Tuple[list, list]:
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_names, process_list = check_node_parents(node=node)
    output_objects = []

    if "data" not in node.arguments:
        raise Exception("Process %s requires parameter <data>" % PROCESS_NAME)

    # Catch the first input
    for data_object in node.get_parent_by_name(parent_name="data").output_objects:
        pc = create_process_chain_entry(data_object=data_object)
        process_list.append(pc)
        break

    for data_object in node.get_parent_by_name(parent_name="data").output_objects:
        output_objects.append(data_object)
        node.add_output(data_object)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
