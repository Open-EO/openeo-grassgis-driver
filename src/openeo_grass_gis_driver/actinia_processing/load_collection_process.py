# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph, ProcessGraphNode

from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, check_node_parents
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2019, Markus Metz, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "load_collection"

# based on get_data, updated to OpenEO API v0.4

def create_process_description():

    p_data = Parameter(description="The identifier of a single raster-, vector- or space-time raster dataset",
                        schema={"type": "string",
                                  "examples": ["nc_spm_08.landsat.raster.lsat5_1987_10",
                                               "nc_spm_08.PERMANENT.vector.lakes",
                                               "ECAD.PERMANENT.strds.temperature_1950_2017_yearly"]},
                          required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    # Example
    arguments = {"id": "latlong_wgs84.modis_ndvi_global.strds.ndvi_16_5600m"}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"load_strds_collection": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="This process returns a raster-, a vector- or a space-time raster "
                                        "datasets that is available in the /collections endpoint.",
                            summary="Returns a single dataset that is available in "
                                    "the /collections endpoint for processing",
                            parameters={"id": p_data},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_name):
    """Create a Actinia process description that uses t.rast.series to create the minimum
    value of the time series.

    :param input_time_series: The input time series name
    :param output_map: The name of the output map
    :return: A Actinia process chain description
    """

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
    input_name = layer_name
    if mapset is not None:
        input_name = layer_name + "@" + mapset

    rn = randint(0, 1000000)

    pc = {}

    if datatype == "raster":
        pc = {"id": "r_info_%i" % rn,
              "module": "r.info",
              "inputs": [{"param": "map", "value": input_name}, ],
              "flags": "g"}
    elif datatype == "vector":
        pc = {"id": "v_info_%i" % rn,
              "module": "v.info",
              "inputs": [{"param": "map", "value": input_name}, ],
              "flags": "g"}
    elif datatype == "strds":
        pc = {"id": "t_info_%i" % rn,
              "module": "t.info",
              "inputs": [{"param": "input", "value": input_name}, ],
              "flags": "g"}
    else:
        raise Exception("Unsupported datatype")

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_names, actinia_process_list)
    """

    input_names, process_list = check_node_parents(node=node)
    output_names = []

    # First analyse the data entry
    if "id" not in node.arguments:
        raise Exception("Process %s requires parameter <id>" % PROCESS_NAME)

    output_names.append(node.arguments["id"])
    node.add_output(node.arguments["id"])

    pc = create_process_chain_entry(input_name=node.arguments["id"])
    process_list.append(pc)

    # Then add the input to the output
    for input_name in input_names:
        # Create the output name based on the input name and method
        output_name = input_name
        output_names.append(output_name)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
