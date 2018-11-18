# -*- coding: utf-8 -*-

# This is the process dictionary that is used to store all processes of the Actinia wrapper
PROCESS_DESCRIPTION_DICT = {}
PROCESS_DICT = {}


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


def analyse_process_graph(graph):
    """Analyse a process graph and call the required subprocess analysis

    This function return the list of input names for the next process and the
    Actinia process chain that was build before.

    :param graph: The process description
    :return: (output_name_list, process_list)
    """

    if graph is None:
        raise Exception("Empty process graph")

    process_list = []
    output_name_list = []

    for key in graph:
        process = graph[key]

        if "process_id" in process:

            if process["process_id"] not in PROCESS_DICT:
                raise Exception("Unsupported process id, available processes: %s"%PROCESS_DICT.keys())

            outputs, processes = PROCESS_DICT[process["process_id"]](process)
            process_list.extend(processes)
            output_name_list.extend(outputs)

    return output_name_list, process_list
