# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, check_node_parents
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue
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
                      schema={"type": "object", "format": "eodata"},
                      required=True)
    p_green = Parameter(description="Any openEO process object that returns raster dataset that should be used as "
                                    "the green channel in the resulting GRB image.",
                        schema={"type": "object", "format": "eodata"},
                        required=True)
    p_blue = Parameter(description="Any openEO process object that returns raster dataset that should be used as "
                                   "the blue channel in the resulting GRB image.",
                       schema={"type": "object", "format": "eodata"},
                       required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    simple_example = {
        "rgb_raster_exporter_1": {
            "process_id": PROCESS_NAME,
            "arguments": {
                "red": {"from_node": "get_red_data"},
                "green": {"from_node": "get_green_data"},
                "blue": {"from_node": "get_blue_data"},
            }
        }
    }

    examples = dict(simple_example=simple_example)

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="This process exports three raster map layers as a single RGB image "
                                        "using the region specified upstream.",
                            summary="Exports three RGB raster map layers using the region specified upstream.",
                            parameters={"red": p_red, "green": p_green, "blur": p_blue},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(output_name: str, red_name: str, green_name: str, blue_name: str) -> list:
    """Actinia process to export an RGB composite GeoTiff

    :param output_name:
    :param red_name:
    :param green_name:
    :param blue_name:
    :return: The process chain
    """

    location, mapset, datatype, red_name = ActiniaInterface.layer_def_to_components(red_name)
    if mapset is not None:
        red_name = red_name + "@" + mapset

    location, mapset, datatype, green_name = ActiniaInterface.layer_def_to_components(green_name)
    if mapset is not None:
        green_name = green_name + "@" + mapset
    location, mapset, datatype, blue_name = ActiniaInterface.layer_def_to_components(blue_name)
    if mapset is not None:
        blue_name = blue_name + "@" + mapset

    rn = randint(0, 1000000)
    pc = []

    composite = {
        "id": "composite_%i" % rn,
        "module": "r.composite",
        "inputs": [{"param": "red", "value": red_name},
                   {"param": "green", "value": green_name},
                   {"param": "blue", "value": blue_name}],
        "outputs": [{"export": {"type": "raster", "format": "GTiff"},
                     "param": "output",
                     "value": output_name}]}
    pc.append(composite)

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_names, actinia_process_list)
    """

    input_names, process_list = check_node_parents(node=node)
    output_names = []

    # First analyse the data entries
    if "red" not in node.arguments:
        raise Exception("Process %s requires parameter <red>" % PROCESS_NAME)
    if "green" not in node.arguments:
        raise Exception("Process %s requires parameter <green>" % PROCESS_NAME)
    if "blue" not in node.arguments:
        raise Exception("Process %s requires parameter <blue>" % PROCESS_NAME)

    # Get the red, green and blue data separately
    red_input_names = node.get_parent_by_name(parent_name="red").output_names
    green_input_names = node.get_parent_by_name(parent_name="green").output_names
    blue_input_names = node.get_parent_by_name(parent_name="blue").output_names

    if not red_input_names:
        raise Exception("Process %s requires an input raster for band <red>" % PROCESS_NAME)
    if not green_input_names:
        raise Exception("Process %s requires an input raster for band <green>" % PROCESS_NAME)
    if not blue_input_names:
        raise Exception("Process %s requires an input raster for band <blue>" % PROCESS_NAME)

    red_name = list(red_input_names)[-1]
    green_name = list(green_input_names)[-1]
    blue_name = list(blue_input_names)[-1]

    output_names.extend(list(red_input_names))
    output_names.extend(list(green_input_names))
    output_names.extend(list(blue_input_names))

    rn = randint(0, 1000000)
    output_name = "red_green_blue_composite_%i" % rn
    output_names.append(output_name)
    node.add_output(output_name=output_name)

    pc = create_process_chain_entry(output_name=output_name, red_name=red_name,
                                    green_name=green_name, blue_name=blue_name)
    process_list.extend(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
