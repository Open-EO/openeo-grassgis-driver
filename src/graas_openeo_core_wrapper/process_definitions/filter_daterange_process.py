# -*- coding: utf-8 -*-
from random import randint
from graas_openeo_core_wrapper import process_definitions
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
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

process_definitions.PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_graas_process_chain_entry(strds_name, start_time, end_time, output_strds_name):
    """Create a GRaaS command of the process chain that uses t.rast.extract to create a subset of a strds

    :param strds_name: The name of the strds
    :param start_time:
    :param end_time:
    :return: A GRaaS process chain description
    """
    # Get info about the time series to extract its resolution settings and bbox
    rn = randint(0, 1000000)

    output_name = "%s_extract"%strds_name.split("@")[0]

    pc = {"id": "t_rast_extract_%i"%rn,
          "module": "t.rast.extract",
          "inputs": [{"param": "input", "value": strds_name},
                     {"param": "where", "value": "start_time >= '%(start)s' "
                                                 "AND end_time <= '%(end)s'"%{"start":start_time, "end":end_time}},
                     {"param": "output", "value": output_strds_name},
                     {"param": "expression", "value": "1.0 * %s"%strds_name},
                     {"param": "basename", "value": output_name},
                     {"param": "suffix", "value": "num"}]}

    return pc


def get_process_list(args):
    """Analyse the process description and return the GRaaS process chain and the name of the processing result
    strds that was filtered by start and end date

    :param args: The process description
    :return: (output_name, pc)
    """

    # Get the input description and the process chain to attach this process
    strds_name, process_list = process_definitions.analyse_process_graph(args)

    # Pipe the input name to the output
    output_strds_name = strds_name[0].split("@")[0] + "_" + PROCESS_NAME

    start_time = None
    end_time = None

    if "from" in args:
        start_time = args["from"]
    if "to" in args:
        end_time = args["to"]

    pc = create_graas_process_chain_entry(strds_name=strds_name[0],
                                          start_time=start_time,
                                          end_time=end_time,
                                          output_strds_name=output_strds_name)
    process_list.append(pc)

    return [output_strds_name,], process_list


process_definitions.PROCESS_DICT[PROCESS_NAME] = get_process_list
