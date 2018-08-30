# -*- coding: utf-8 -*-
from random import randint
from .base import analyse_process_graph, PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from .actinia_interface import ActiniaInterface


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
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

PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_process_chain_entry(input_name, output_name):
    """Create a GRaaS process description that uses t.rast.series to create the minimum
    value of the time series.

    :param input_time_series: The input time series name
    :param output_map: The name of the output map
    :return: A GRaaS process chain description
    """

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
    input_name = layer_name
    if mapset is not None:
        input_name = layer_name + "@" + mapset

    rn = randint(0, 1000000)

    pc = {"id": "t_rast_series_%i"%rn,
          "module": "t.rast.series",
          "inputs": [{"param": "input", "value": input_name},
                     {"param": "method", "value": "minimum"},
                     {"param": "output", "value": output_name}],
          "flags": "t"}

    return pc


def get_process_list(args):
    """Analyse the process description and return the GRaaS process chain and the name of the processing result layer
    which is a single raster layer

    :param args: The process description arguments
    :return: (output_name, pc)
    """
    input_names, process_list = analyse_process_graph(args)
    output_names = []

    for input_name in input_names:
        location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
        output_name = "%s_%s" % (layer_name, PROCESS_NAME)
        output_names.append(output_name)

        pc = create_process_chain_entry(input_name,
                                              output_name)
        process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
