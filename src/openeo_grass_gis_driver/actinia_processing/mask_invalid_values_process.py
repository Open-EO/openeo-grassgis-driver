# -*- coding: utf-8 -*-
import json
from random import randint
from typing import List, Tuple

from openeo_grass_gis_driver.actinia_processing.base import check_node_parents
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue
from .base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "mask_invalid_values"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)
    p_min = Parameter(description="Minimum allowed value",
                       schema={"type": "object", "format": "float"},
                       required=True)
    p_max = Parameter(description="Maximum allowed value",
                        schema={"type": "object", "format": "float"},
                        required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    examples = dict(simple={
        "mask_invalid_values_1": {
            "process_id": PROCESS_NAME,
            "arguments": {
                "data": {"from_node": "get_data_1"},
                "min": 1,
                "max": 150,
            }
        }
    })

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Drops observations from raster data or raster time series data "
                                        " that are outside of the specified interval.",
                            summary="Filter raster based data on the specified interval",
                            parameters={"data": p_data,
                                        "min": p_min,
                                        "max": p_max},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_time_series, vmin, vmax, output_time_series):
    """Create a Actinia command of the process chain that uses t.rast.mapcalc 
    to filter raster values by the specified interval

    :param input_time_series: The input time series name
    :param min: smallest allowed value 
    :param max: largest allowed value
    :param output_time_series: The output time series name
    :return: A Actinia process chain description
    """

    input_name = ActiniaInterface.layer_def_to_grass_map_name(input_time_series)
    output_name = ActiniaInterface.layer_def_to_grass_map_name(output_time_series)

    rn = randint(0, 1000000)

    pc = {"id": "t_rast_mapcalc_%i" % rn,
         "module": "t.rast.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = if(%(raw)s < %(min)s || "
                              "%(raw)s > %(max)s), null(), %(raw)s)" % {"result": output_name,
                                                        "raw": input_name,
                                                        "min": str(vmin),
                                                        "max": str(vmax)}},
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
            "min" not in node.arguments or \
            "max" not in node.arguments:
        raise Exception("Process %s requires parameter data, min, max" % PROCESS_NAME)

    vmin = node.arguments["min"]
    vmax = node.arguments["max"]

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_names)
    output_name = "%s_%s" % (layer_name, PROCESS_NAME)
    output_names.append(output_name)
    node.add_output(output_name=output_name)

    pc = create_process_chain_entry(input_names, vmin, vmax, output_name)
    process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
