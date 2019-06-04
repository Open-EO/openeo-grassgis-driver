# -*- coding: utf-8 -*-
import json
from random import randint
from typing import List, Tuple

from openeo_grass_gis_driver.actinia_processing.base import check_node_parents
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue
from .base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "scale_minmax"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)
    p_min = Parameter(description="New minimum value",
                       schema={"type": "object", "format": "float"},
                       required=True)
    p_max = Parameter(description="New maximum value",
                        schema={"type": "object", "format": "float"},
                        required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    examples = dict(simple={
        "scale_minmax_1": {
            "process_id": PROCESS_NAME,
            "arguments": {
                "data": {"from_node": "get_data_1"},
                "min": 1,
                "max": 255,
            }
        }
    })

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Scales the image values between specified min and max values.",
                            summary="Rescale raster based data on interval",
                            parameters={"data": p_data,
                                        "min": p_min,
                                        "max": p_max,
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_time_series, newmin, newmax, output_time_series):
    """Create a Actinia command of the process chain that uses t.rast.mapcalc 
    to rescale raster values to the specified interval

    :param min:
    :param max:
    :return: A Actinia process chain description
    """

    input_name = ActiniaInterface.layer_def_to_grass_map_name(input_time_series)
    output_name = ActiniaInterface.layer_def_to_grass_map_name(output_time_series)

    rn = randint(0, 1000000)

    # TODO: get min, max for input raster with r.info -r,
    # these are oldmin, oldmax

    pc = {"id": "r_mapcalc_%i" % rn,
         "module": "r.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = ((%(raw)s - %(rmin)s) / (%(rmax)s - %(rmin)s)) * "
                              "(%(max)s - %(min)s) + %(min)s" % {"result": output_name,
                                                        "raw": input_name,
                                                        "rmin": str(oldmin),
							"rmax": str(oldmax)}},
                                                        "min": str(newmin),
							"max": str(newmax)}},
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

    min = node.arguments["min"]
    max = node.arguments["max"]

    # for each raster separately
    for input_name in node.get_parent_by_name("data").output_names:
	location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
	output_name = "%s_%s" % (layer_name, PROCESS_NAME)
	output_names.append(output_name)
	node.add_output(output_name=output_name)

	pc = create_process_chain_entry(input_names, min=min, max=max, output_names)
	process_list.append(pc)

    # TODO: create strds from output raster maps

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
