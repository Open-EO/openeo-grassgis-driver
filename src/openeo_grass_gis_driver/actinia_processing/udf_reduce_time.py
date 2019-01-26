# -*- coding: utf-8 -*-
from .base import analyse_process_graph, PROCESS_DICT_LEGACY, PROCESS_DESCRIPTION_DICT_LEGACY
from .actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "udf_reduce_time"

DOC = {
    "process_id": PROCESS_NAME,
    "description": "Apply a user defined function (UDF) to a time series of raster layers"
                   " that produces a single raster layer as output.",
    "args": {
        "collections": {
            "description": "array of input collections with one element"
        },
        "python_file_url": {
            "description": "The public URL to the python file that contains the udf"
        }
    }
}

PROCESS_DESCRIPTION_DICT_LEGACY[PROCESS_NAME] = DOC


def create_process_chain_entry(input_name, python_file_url, output_name):
    """Create a Actinia command of the process chain that uses g.region to create a valid computational region
    for the provide input strds

    :param strds_name: The name of the strds
    :param python_file_url: The URL to the python file that defines the UDF
    :param output_name: The name of the output raster layer
    :return: A Actinia process chain description
    """

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
    input_name = layer_name
    if mapset is not None:
        input_name = layer_name + "@" + mapset

    pc = {"id": "t_rast_aggr_func",
          "module": "t.rast.aggr_func",
          "inputs": [{"import_descr": {"source": python_file_url,
                                       "type": "file"},
                      "param": "pyfile",
                      "value": "$file::my_py_func"},
                     {"param": "input",
                      "value": input_name},
                     {"param": "output",
                      "value": output_name}]}

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

        location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
        output_name = "%s_%s" % (layer_name, PROCESS_NAME)
        output_names.append(output_name)

        if "python_file_url" in args:
            python_file_url = args["python_file_url"]
        else:
            raise Exception("Python file is missing in the process description")

        pc = create_process_chain_entry(input_name=input_name,
                                        python_file_url=python_file_url,
                                        output_name=output_name)
        process_list.append(pc)

    return output_names, process_list


PROCESS_DICT_LEGACY[PROCESS_NAME] = get_process_list
