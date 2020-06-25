# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
    check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "rgb_raster_exporter"


def create_process_description():
    p_red = Parameter(description="Any openEO process object that returns raster dataset that should be used as "
                                  "the red channel in the resulting GRB image.",
                      schema={"type": "object", "format": "raster-cube"},
                      required=True)
    p_green = Parameter(description="Any openEO process object that returns raster dataset that should be used as "
                                    "the green channel in the resulting GRB image.",
                        schema={"type": "object", "format": "raster-cube"},
                        required=True)
    p_blue = Parameter(description="Any openEO process object that returns raster dataset that should be used as "
                                   "the blue channel in the resulting GRB image.",
                       schema={"type": "object", "format": "raster-cube"},
                       required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "raster-cube"})

     # Example
    arguments = {"red": {"from_node": "get_red_data"},
                 "green": {"from_node": "get_green_data"},
                 "blue": {"from_node": "get_blue_data"}}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"rgb_raster_exporter_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="This process exports three raster map layers as a single RGB image "
                                        "using the region specified upstream.",
                            summary="Exports three RGB raster map layers using the region specified upstream.",
                            parameters={"red": p_red, "green": p_green, "blur": p_blue},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(output_object: DataObject, red_object: DataObject,
                               green_object: DataObject, blue_object: DataObject) -> list:
    """Actinia process to export an RGB composite GeoTiff

    :param output_object:
    :param red_name:
    :param green_name:
    :param blue_name:
    :return: The process chain
    """

    rn = randint(0, 1000000)
    pc = []

    composite = {
        "id": "composite_%i" % rn,
        "module": "r.composite",
        "inputs": [{"param": "red", "value": red_object.grass_name()},
                   {"param": "green", "value": green_object.grass_name()},
                   {"param": "blue", "value": blue_object.grass_name()}],
        "outputs": [{"export": {"type": "raster", "format": "GTiff"},
                     "param": "output",
                     "value": output_object.grass_name()}]}
    pc.append(composite)

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    # First analyse the data entries
    if "red" not in node.arguments:
        raise Exception("Process %s requires parameter <red>" % PROCESS_NAME)
    if "green" not in node.arguments:
        raise Exception("Process %s requires parameter <green>" % PROCESS_NAME)
    if "blue" not in node.arguments:
        raise Exception("Process %s requires parameter <blue>" % PROCESS_NAME)

    # Get the red, green and blue data separately
    red_input_objects = node.get_parent_by_name(parent_name="red").output_objects
    green_input_objects = node.get_parent_by_name(parent_name="green").output_objects
    blue_input_objects = node.get_parent_by_name(parent_name="blue").output_objects

    if not red_input_objects:
        raise Exception("Process %s requires an input raster for band <red>" % PROCESS_NAME)
    if not green_input_objects:
        raise Exception("Process %s requires an input raster for band <green>" % PROCESS_NAME)
    if not blue_input_objects:
        raise Exception("Process %s requires an input raster for band <blue>" % PROCESS_NAME)

    red_object = list(red_input_objects)[-1]
    green_object = list(green_input_objects)[-1]
    blue_object = list(blue_input_objects)[-1]

    output_objects.extend(list(red_input_objects))
    output_objects.extend(list(green_input_objects))
    output_objects.extend(list(blue_input_objects))

    rn = randint(0, 1000000)

    output_object = DataObject(name="red_green_blue_composite_%i" % rn, datatype=GrassDataType.STRDS)
    output_objects.append(output_object)
    node.add_output(output_object=output_object)

    pc = create_process_chain_entry(output_object=output_object, red_object=red_object,
                                    green_object=green_object, blue_object=blue_object)
    process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
