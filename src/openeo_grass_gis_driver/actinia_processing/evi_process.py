# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph, ProcessGraphNode

from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
    check_node_parents
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2019, Markus Metz, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "evi"


def create_process_description():
    p_red = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                                  "that contains the RED band for EVI computation.",
                      schema={"type": "object", "format": "eodata"},
                      required=True)

    p_nir = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                                  "that contains the NIR band for EVI computation.",
                      schema={"type": "object", "format": "eodata"},
                      required=True)

    p_blue = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                                  "that contains the BLUE band for EVI computation.",
                      schema={"type": "object", "format": "eodata"},
                      required=True)

    p_scale = Parameter(description="Scale factor to convert band values",
                        schema={"type": "object", "format": "float"},
                        required=False)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    # Example
    arguments = {
        "red": {"from_node": "get_red_data"},
        "nir": {"from_node": "get_nir_data"},
        "blue": {"from_node": "get_blue_data"},
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"evi_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Compute the EVI based on the red, nir, and blue bands of the input datasets.",
                            summary="Compute the EVI based on the red, nir, and blue bands of the input datasets.",
                            parameters={"red": p_red, "nir": p_nir, "blue": p_blue, "scale": p_scale},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(nir_time_series, red_time_series, blue_time_series, scale, output_time_series):
    """Create a Actinia process description that uses t.rast.mapcalc to create the EVI time series

    :param nir_time_series: The NIR band time series name
    :param red_time_series: The RED band time series name
    :param blue_time_series: The BLUE band time series name
    :param scale: scale factor
    :param output_time_series: The name of the output time series
    :return: A list of Actinia process chain descriptions
    """
    nir_time_series = ActiniaInterface.layer_def_to_grass_map_name(nir_time_series)
    red_time_series = ActiniaInterface.layer_def_to_grass_map_name(red_time_series)
    blue_time_series = ActiniaInterface.layer_def_to_grass_map_name(blue_time_series)
    output_name = ActiniaInterface.layer_def_to_grass_map_name(output_time_series)

    rn = randint(0, 1000000)

    pc = [
        {"id": "t_rast_mapcalc_%i" % rn,
         "module": "t.rast.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = float(2.5 * %(scale)s * (%(nir)s - %(red)s)/"
                              "(%(nir)s * %(scale)s + 6.0 * %(red)s * %(scale)s -7.5 * %(blue)s * %(scale)s + 1.0))" % {
                                                        "result": output_name,
                                                        "nir": nir_time_series,
                                                        "red": red_time_series,
                                                        "blue": blue_time_series,
                                                        "scale": scale}},
                    {"param": "inputs",
                     "value": "%(nir)s,%(red)s,%(blue)s" % {"nir": nir_time_series,
                                                            "red": red_time_series,
                                                            "blue": blue_time_series}},
                    {"param": "basename",
                     "value": "evi"},
                    {"param": "output",
                     "value": output_name}]},
        {"id": "t_rast_color_%i" % rn,
         "module": "t.rast.colors",
         "inputs": [{"param": "input",
                     "value": output_name},
                    {"param": "color",
                     "value": "ndvi"}]}]

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

    if "nir" not in node.arguments:
        raise Exception("Process %s requires parameter <nir>" % PROCESS_NAME)

    if "blue" not in node.arguments:
        raise Exception("Process %s requires parameter <blue>" % PROCESS_NAME)

    # Get the red and nir data separately
    red_input_names = node.get_parent_by_name(parent_name="red").output_names
    nir_input_names = node.get_parent_by_name(parent_name="nir").output_names
    blue_input_names = node.get_parent_by_name(parent_name="blue").output_names

    if not red_input_names:
        raise Exception("Process %s requires an input strds for band <red>" % PROCESS_NAME)

    if not nir_input_names:
        raise Exception("Process %s requires an input strds for band <nir>" % PROCESS_NAME)

    if not blue_input_names:
        raise Exception("Process %s requires an input strds for band <blue>" % PROCESS_NAME)

    scale = 1.0
    if "scale" in node.arguments:
        scale = float(node.arguments["scale"])

    red_strds = list(red_input_names)[-1]
    nir_strds = list(nir_input_names)[-1]
    blue_strds = list(blue_input_names)[-1]

    output_names.extend(list(red_input_names))
    output_names.extend(list(nir_input_names))
    output_names.extend(list(blue_input_names))

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(red_strds)
    output_name = "%s_%s" % (layer_name, PROCESS_NAME)
    output_names.append(output_name)
    node.add_output(output_name=output_name)

    pc = create_process_chain_entry(nir_strds, red_strds, blue_strds, scale, output_name)
    process_list.extend(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
