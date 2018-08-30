# -*- coding: utf-8 -*-
from random import randint
from .base import analyse_process_graph, PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from .actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


PROCESS_NAME = "filter_daterange"

DOC = {
    "process_id": PROCESS_NAME,
    "description": "Drops observations from a collection that have been captured before"
                   " a start or after a given end date.",
    "args": {
        "collections": {
            "description": "array of input collections with one element"
        },
        "from": {
            "description": "start date"
        },
        "to": {
            "description": "end date"
        }
    }
}

PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create__process_chain_entry(input_name, start_time, end_time, output_name):
    """Create a Actinia command of the process chain that uses t.rast.extract to create a subset of a strds

    :param strds_name: The name of the strds
    :param start_time:
    :param end_time:
    :return: A Actinia process chain description
    """
    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
    input_name = layer_name
    if mapset is not None:
        input_name = layer_name + "@" + mapset
    base_name = "%s_extract"%layer_name

    # Get info about the time series to extract its resolution settings and bbox
    rn = randint(0, 1000000)


    pc = {"id": "t_rast_extract_%i"%rn,
          "module": "t.rast.extract",
          "inputs": [{"param": "input", "value": input_name},
                     {"param": "where", "value": "start_time >= '%(start)s' "
                                                 "AND end_time <= '%(end)s'"%{"start":start_time, "end":end_time}},
                     {"param": "output", "value": output_name},
                     {"param": "expression", "value": "1.0 * %s"%input_name},
                     {"param": "basename", "value": base_name},
                     {"param": "suffix", "value": "num"}]}

    return pc


def get_process_list(args):
    """Analyse the process description and return the Actinia process chain and the name of the processing result
    strds that was filtered by start and end date

    :param args: The process description
    :return: (output_name, pc)
    """

    # Get the input description and the process chain to attach this process
    input_names, process_list = analyse_process_graph(args)
    output_names = []

    for input_name in input_names:

        location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
        output_name = "%s_%s" % (layer_name, PROCESS_NAME)
        output_names.append(output_name)

        start_time = None
        end_time = None

        if "from" in args:
            start_time = args["from"]
        if "to" in args:
            end_time = args["to"]

        pc = create__process_chain_entry(input_name=input_name,
                                         start_time=start_time,
                                         end_time=end_time,
                                         output_name=output_name)
        process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
