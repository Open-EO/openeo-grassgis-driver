# -*- coding: utf-8 -*-

# This is the process dictionary that is used to store all processes of the GRaaS wrapper
PROCESS_DESCRIPTION_DICT = {}
PROCESS_DICT = {}

# Import the process_definitions to fill the process.PROCESS_DICT with process_definitions
import graas_openeo_core_wrapper.process_definitions.filter_bbox_process
import graas_openeo_core_wrapper.process_definitions.filter_daterange_process
import graas_openeo_core_wrapper.process_definitions.ndvi_process
import graas_openeo_core_wrapper.process_definitions.min_time_process


def check_leaf(leaf):
    """Check a process description and call the required subprocess analysis

    :param leaf: The process description
    :return: (output_name, pc)
    """

    if "collections" not in leaf and "process_graph" not in leaf:
        raise Exception("process_graph or collection not found on process description")

    process_list = []
    input_name = ""

    if "collections" in leaf:
        if len(leaf["collections"]) != 1:
            raise Exception("A single entry is expected in the collection of the process description")
        entry = leaf["collections"][0]

    if "process_graph" in leaf:
        entry = leaf["process_graph"]

    if "process_id" in entry:
        input_name, process_list = PROCESS_DICT[entry["process_id"]](entry["args"])
    if "product_id" in entry:
        input_name = entry["product_id"]

    return input_name, process_list
