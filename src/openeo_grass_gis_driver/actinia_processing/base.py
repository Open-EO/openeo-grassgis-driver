# -*- coding: utf-8 -*-

# This is the process dictionary that is used to store all processes of the Actinia wrapper
PROCESS_DESCRIPTION_DICT = {}
PROCESS_DICT = {}


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def analyse_process_graph(graph):
    """Analyse a process process graph and call the required subprocess analysis

    This function return the list of input names for the next process and the
    GRaaS process chain that was build before.

    :param graph: The process description
    :return: (output_name_list, pc)
    """

    if not graph or ("collections" not in graph and "process_graph" not in graph):
        raise Exception("process_graph or collection not found on process description")

    process_list = []
    input_list = []

    if "process_graph" in graph:
        entry = graph["process_graph"]

        if "process_id" in entry:

            if entry["process_id"] not in PROCESS_DICT:
                raise Exception("Unsupported process id")

            inputs, processes = PROCESS_DICT[entry["process_id"]](entry["args"])
            process_list.extend(processes)
            input_list.extend(inputs)
        if "product_id" in entry:
            input = entry["product_id"]
            input_list.append(input)

    elif "collections" in graph:
        entry_list = graph["collections"]
        for entry in entry_list:

            if "process_id" in entry:

                if entry["process_id"] not in PROCESS_DICT:
                    raise Exception("Unsupported process id")

                inputs, processes = PROCESS_DICT[entry["process_id"]](entry["args"])
                process_list.extend(processes)
                input_list.extend(inputs)
            if "product_id" in entry:
                inputs = entry["product_id"]
                input_list.append(inputs)

    return input_list, process_list
