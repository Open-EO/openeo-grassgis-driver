# -*- coding: utf-8 -*-

# This is the process dictionary that is used to store all processes of the GRaaS wrapper
PROCESS_DESCRIPTION_DICT = {}
PROCESS_DICT = {}

# Import the process_definitions to fill the process.PROCESS_DICT with process_definitions
import graas_openeo_core_wrapper.process_definitions.filter_bbox_process
import graas_openeo_core_wrapper.process_definitions.filter_daterange_process
import graas_openeo_core_wrapper.process_definitions.ndvi_process
import graas_openeo_core_wrapper.process_definitions.min_time_process


def analyse_process_graph(args):
    """Analyse a process process graph and call the required subprocess analysis

    This function return the list of input names for the next process and the
    GRaaS process chain that was build before.

    :param args: The process description
    :return: (output_name_list, pc)
    """

    if not args or ("collections" not in args and "process_graph" not in args):
        raise Exception("process_graph or collection not found on process description")

    process_list = []
    input_list = []

    if "process_graph" in args:
        entry = args["process_graph"]

        if "process_id" in entry:

            if entry["process_id"] not in PROCESS_DICT:
                raise Exception("Unsupported process id")

            inputs, processes = PROCESS_DICT[entry["process_id"]](entry["args"])
            process_list.extend(processes)
            input_list.extend(inputs)
        if "product_id" in entry:
            input = entry["product_id"]
            input_list.append(input)

    elif "collections" in args:
        entry_list = args["collections"]
        for entry in entry_list:

            if "process_id" in entry:
                inputs, processes = PROCESS_DICT[entry["process_id"]](entry["args"])

                if entry["process_id"] not in PROCESS_DICT:
                    raise Exception("Unsupported process id")

                process_list.extend(processes)
                input_list.extend(inputs)
            if "product_id" in entry:
                inputs = entry["product_id"]
                input_list.append(inputs)

    return input_list, process_list
