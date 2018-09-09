# -*- coding: utf-8 -*-
from random import randint
from .base import analyse_process_graph, PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from .actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "reduce_time"

DOC = {
    "process_id": PROCESS_NAME,
    "description": "Reduce the time dimension of a space-time raster dataset "
                   "with different reduce options.",
    "parameters":
        {
            "imagery":
                {
                    "description": "Any openEO process object that returns space-time raster datasets",
                    "schema":
                        {
                            "type": "object",
                            "format": "eodata"
                        }
                },
            "method":
                {
                    "description": "The method to reduce the time dimension of a "
                                   "space-time raster dataset",
                    "schema":
                        {
                            "type": "string"
                        },
                    "enum": ["average", "count", "median", "mode", "minimum", "min_raster", "maximum",
                             "max_raster", "stddev", "range,sum", "variance", "diversity", "slope",
                             "offset", "detcoeff", "quart1", "quart3", "perc90", "quantile", "skewness",
                             "kurtosis"]
                }
        },
    "returns":
        {
            "description": "Processed EO data.",
            "schema":
                {
                    "type": "object",
                    "format": "eodata"
                }
        },
    "examples": [
        {
            "process_id": PROCESS_NAME,
            "method": "average",
            "imagery": {
                "process_id": "get_data",
                "data_id": "ECAD.PERMANENT.strds.temperature_1950_2017_yearly"
            }
        }
    ]
}

PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_process_chain_entry(input_name, method, output_name):
    """Create a Actinia process description that uses t.rast.series to reduce a time series.

    :param input_time_series: The input time series name
    :param method: The method for time reduction
    :param output_map: The name of the output map
    :return: A Actinia process chain description
    """
    input_name = ActiniaInterface.layer_def_to_grass_map_name(input_name)

    rn = randint(0, 1000000)

    pc = {"id": "t_rast_series_%i" % rn,
          "module": "t.rast.series",
          "inputs": [{"param": "input", "value": input_name},
                     {"param": "method", "value": method},
                     {"param": "output", "value": output_name}],
          "flags": "t"}

    return pc


def get_process_list(process):
    """Analyse the process description and return the Actinia process chain
    and the name of the processing result layer
    which is a single raster layer

    :param args: The process description arguments
    :return: (output_names, actinia_process_list)
    """
    input_names, process_list = analyse_process_graph(process)
    output_names = []

    if "method" not in process:
        raise Exception("Parameter method is required.")

    for input_name in input_names:
        location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
        output_name = "%s_%s" % (layer_name, PROCESS_NAME)
        output_names.append(output_name)

        pc = create_process_chain_entry(input_name, process["method"], output_name)
        process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
