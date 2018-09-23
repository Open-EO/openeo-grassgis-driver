# -*- coding: utf-8 -*-
from random import randint
from .base import analyse_process_graph, PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from .actinia_interface import ActiniaInterface


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "raster_exporter"

DOC = {
    "name": PROCESS_NAME,
    "summary": "Exports raster map layers using the region specified upstream.",
    "description": "This process exports an arbitrary number of raster map layers "
                   "using the region specified upstream.",
    "parameters":
        {
            "imagery":
                {
                    "description": "Any openEO process object that returns raster datasets, "
                                   "vector datasets or space-time raster dataset",
                    "schema":
                        {
                            "type": "object",
                            "format": "eodata"
                        }
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
            "imagery": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.PERMANENT.vector.lakes"
            }
        }
    ]
}

PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_process_chain_entry(input_name):
    """Create a Actinia command of the process chain that computes the regional statistics based on a
    strds and a polygon.

    :param input_name: The name of the raster layer
    :return: A Actinia process chain description
    """

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
    input_name = layer_name
    if mapset is not None:
        input_name = layer_name + "@" + mapset

    rn = randint(0, 1000000)
    pc = []

    exporter = {
        "id": "exporter_%i"%rn,
          "module": "exporter",
          "outputs": [{"export": {"type": "raster", "format": "GTiff"},
                       "param": "map",
                       "value": input_name}]}

    pc.append(exporter)

    return pc


def get_process_list(args):
    """Analyse the process description and return the Actinia process chain and the name of the processing result layer
    which is a single raster layer

    :param args: The process description
    :return: (output_names, actinia_process_list)
    """

    # Get the input description and the process chain to attach this process
    input_names, process_list = analyse_process_graph(args)
    output_names = []

    for input_name in input_names:

        output_name = input_name
        output_names.append(output_name)

        pc = create_process_chain_entry(input_name=input_name)
        process_list.extend(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
