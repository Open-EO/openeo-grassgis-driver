# -*- coding: utf-8 -*-
from random import randint
from graas_openeo_core_wrapper import process_definitions

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


PROCESS_NAME = "min_time"

DOC = {
    "process_id": PROCESS_NAME,
    "description": "Finds the minimum value of time series for all bands of the input dataset.",
    "args": {
        "collections": {
            "description": "array of input collections with one element"
        },
    }
}

process_definitions.PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_graas_process_chain_entry(input_time_series, output_map):
    """Create a GRaaS process description that uses t.rast.series to create the minimum
    value of the time series.

    :param input_time_series: The input time series name
    :param output_map: The name of the output map
    :return: A GRaaS process chain description
    """
    rn = randint(0, 1000000)

    pc = {"id": "t_rast_series_%i"%rn,
          "module": "t.rast.series",
          "inputs": [{"param": "input", "value": input_time_series},
                     {"param": "method", "value": "minimum"},
                     {"param": "output", "value": output_map}],
          "flags": "t"}

    return pc


def get_process_list(args):
    """Analyse the process description and return the GRaaS process chain and the name of the processing result layer
    which is a single raster layer

    :param args: The process description arguments
    :return: (output_name, pc)
    """
    input_name, process_list = process_definitions.analyse_process_graph(args)

    # Create the output name based on the input name and method
    output_name = input_name[0] + "_" + PROCESS_NAME

    pc = create_graas_process_chain_entry(input_name[0],
                                          output_name)
    process_list.append(pc)

    return [output_name,], process_list


process_definitions.PROCESS_DICT[PROCESS_NAME] = get_process_list
