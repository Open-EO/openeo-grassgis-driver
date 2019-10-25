# -*- coding: utf-8 -*-
import json
from random import randint
from typing import List, Tuple

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import check_node_parents
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from .base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "mask"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)
    p_mask = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)
    p_value = Parameter(description="The value used to replace non-zero and `true` values with",
                       schema={"type": "object", "format": "string"},
                       required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    # Example
    arguments = {
                "data": {"from_node": "get_data_1"},
                "mask": {"from_node": "get_data_2"},
                "value": "null",
            }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"mask_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Applies a mask to a raster data cube "
                                        " replacing values in data that are not null in mask with the new value.",
                            summary="Applies a mask to a raster data cube",
                            parameters={"data": p_data,
                                        "mask": p_mask,
                                        "value": p_value},
                            returns=rv,
                            examples=[examples])

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_time_series, mask_time_series, mask_value, output_time_series):
    """Create a Actinia command of the process chain that uses t.rast.mapcalc 
    to mask raster values based on a mask dataset and a replacement value

    :param input_time_series: The input time series name
    :param mask_time_series: time series to use as mask 
    :param mask_value: values in input are replaced with this value if mask is not null
    :param output_time_series: The output time series name
    :return: A Actinia process chain description
    """

    input_name = ActiniaInterface.layer_def_to_grass_map_name(input_time_series)
    mask_name = ActiniaInterface.layer_def_to_grass_map_name(mask_time_series)
    output_name = ActiniaInterface.layer_def_to_grass_map_name(output_time_series)

    rn = randint(0, 1000000)

    if mask_value == "null":
        pc = {"id": "t_rast_mapcalc_%i" % rn,
             "module": "t.rast.mapcalc",
             "inputs": [{"param": "expression",
                         "value": "%(result)s = if(isnull(%(mask_name)s), "
                                  "%(raw)s, null())" % {"result": output_name,
                                                        "mask_name": mask_name,
                                                        "raw": input_name}},
                        {"param": "basename",
                         "value": "masked"},
                        {"param": "output",
                         "value": output_name},
                       ]}
    else:
        pc = {"id": "t_rast_mapcalc_%i" % rn,
             "module": "t.rast.mapcalc",
             "inputs": [{"param": "expression",
                         "value": "%(result)s = if(isnull(%(mask_name)s), "
                                  "%(raw)s, %(mask_value)s)" % {"result": output_name,
                                                        "mask_name": mask_name,
                                                        "raw": input_name,
                                                        "mask_value": mask_value}},
                        {"param": "basename",
                         "value": "masked"},
                        {"param": "output",
                         "value": output_name},
                       ]}

    return pc


def get_process_list(node: Node) -> Tuple[list, list]:
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_names, actinia_process_list)
    """

    input_names, process_list = check_node_parents(node=node)
    output_names = []

    if "data" not in node.arguments or \
            "mask" not in node.arguments or \
            "value" not in node.arguments:
        raise Exception("Process %s requires parameter data, mask, value" % PROCESS_NAME)

    mask_value = node.arguments["value"]
    mask_names = node.arguments["mask"]

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_names)
    output_name = "%s_%s" % (layer_name, PROCESS_NAME)
    output_names.append(output_name)
    node.add_output(output_object=output_name)

    pc = create_process_chain_entry(input_names, mask_names, mask_value, output_name)
    process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
