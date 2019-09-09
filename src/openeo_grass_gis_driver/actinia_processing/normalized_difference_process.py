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
__copyright__ = "Copyright 2018, Markus Metz, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "normalized_difference"


def create_process_description():
    p_band1 = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                                  "that contains the first band for normalized difference computation.",
                      schema={"type": "object", "format": "eodata"},
                      required=True)

    p_band2 = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                                  "that contains the second band for normalized difference computation.",
                      schema={"type": "object", "format": "eodata"},
                      required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    # Example
    arguments = {
        "band1": {"from_node": "get_band1_data"},
        "band2": {"from_node": "get_band2_data"},
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"nnormalized difference_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="The normalized difference is computed as *(band1 - band2) / (band1 + band2).",
                            summary="The normalized difference is computed as *(band1 - band2) / (band1 + band2).",
                            parameters={"band1": p_band1, "band2": p_band2},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(band1_time_series, band2_time_series, output_time_series):
    """Create a Actinia process description that uses t.rast.mapcalc to create the normalized difference time series

    :param band1_time_series: The first band time series name
    :param band2_time_series: The second band time series name
    :param output_time_series: The name of the output time series
    :return: A list of Actinia process chain descriptions
    """
    band1_time_series = ActiniaInterface.layer_def_to_grass_map_name(band1_time_series)
    band2_time_series = ActiniaInterface.layer_def_to_grass_map_name(band2_time_series)
    output_name = ActiniaInterface.layer_def_to_grass_map_name(output_time_series)

    rn = randint(0, 1000000)

    pc = [
        {"id": "t_rast_mapcalc_%i" % rn,
         "module": "t.rast.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = float((%(band1)s - %(band2)s)/"
                              "(%(band1)s + %(band2)s))" % {"result": output_name,
                                                        "band1": band1_time_series,
                                                        "band2": band2_time_series}},
                    {"param": "inputs",
                     "value": "%(band1)s,%(band2)s" % {"band1": band1_time_series,
                                                   "band2": band2_time_series}},
                    {"param": "basename",
                     "value": "nd"},
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
    if "band1" not in node.arguments:
        raise Exception("Process %s requires parameter <band1>" % PROCESS_NAME)

    if "band2" not in node.arguments:
        raise Exception("Process %s requires parameter <band2>" % PROCESS_NAME)

    # Get the red and nir data separately
    band1_input_names = node.get_parent_by_name(parent_name="band1").output_names
    band2_input_names = node.get_parent_by_name(parent_name="band2").output_names

    if not band1_input_names:
        raise Exception("Process %s requires an input strds for band 1" % PROCESS_NAME)

    if not band2_input_names:
        raise Exception("Process %s requires an input strds for band 2" % PROCESS_NAME)

    band1_strds = list(band1_input_names)[-1]
    band2_strds = list(band2_input_names)[-1]

    output_names.extend(list(band1_input_names))
    output_names.extend(list(band2_input_names))

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(band1_strds)
    output_name = "%s_%s" % (layer_name, PROCESS_NAME)
    output_names.append(output_name)
    node.add_output(output_name=output_name)

    pc = create_process_chain_entry(band1_strds, band2_strds, output_name)
    process_list.extend(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
