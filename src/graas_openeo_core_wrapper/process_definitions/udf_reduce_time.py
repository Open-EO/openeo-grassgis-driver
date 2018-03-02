# -*- coding: utf-8 -*-
from graas_openeo_core_wrapper import process_definitions
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from random import randint

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
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

process_definitions.PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_graas_process_chain_entry(strds_name, python_file_url, output_name):
    """Create a GRaaS command of the process chain that uses g.region to create a valid computational region
    for the provide input strds

    :param strds_name: The name of the strds
    :param left:
    :param right:
    :param top:
    :param bottom:
    :return: A GRaaS process chain description
    """

    pc = {"id": "t_rast_aggr_func",
          "module": "t.rast.aggr_func",
          "inputs": [{"import_descr": {"source": python_file_url,
                                       "type": "file"},
                      "param": "pyfile",
                      "value": "$file::my_py_func"},
                     {"param": "input",
                      "value": strds_name},
                     {"param": "output",
                      "value": output_name}]}

    return pc


def get_process_list(args):
    """Analyse the process description and return the GRaaS process chain and the name of the processing result layer
    which is a single raster layer

    :param args: The process description
    :return: (output_name, pc)
    """

    # Get the input description and the process chain to attach this process
    input_names, process_list = process_definitions.analyse_process_graph(args)
    output_names = []

    for input_name in input_names:

        # Create the output name based on the input name and method
        output_name = input_name.split("@")[0] + "_" + PROCESS_NAME
        output_names.append(output_name)

        if "python_file_url" in args:
            python_file_url = args["python_file_url"]
        else:
            raise Exception("Python fle is missing in the process description")

        pc = create_graas_process_chain_entry(strds_name=input_name, python_file_url=python_file_url,
                                              output_name=output_name)
        process_list.append(pc)

    return output_names, process_list


process_definitions.PROCESS_DICT[PROCESS_NAME] = get_process_list
