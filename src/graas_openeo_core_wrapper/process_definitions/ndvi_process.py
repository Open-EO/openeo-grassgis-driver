# -*- coding: utf-8 -*-
from random import randint
from graas_openeo_core_wrapper import process_definitions

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "NDVI"

DOC = {
    "process_id": PROCESS_NAME,
    "description": "Compute the NDVI based on the red and nir bands of the input dataset.",
    "args": {
        "collections": {
            "description": "array of input collections with one element"
        },
        "red": {
            "description": "reference to the red band"
        },
        "nir": {
            "description": "reference to the nir band"
        }
    }
}

process_definitions.PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_graas_process_chain_entry(nir_time_series, red_time_series, output_time_series):
    """Create a GRaaS process description that uses t.rast.series to create the minimum
    value of the time series.

    :param nir_time_series: The NIR band time series name
    :param red_time_series: The RED band time series name
    :param output_time_series: The name of the output time series
    :return: A list of GRaaS process chain descriptions
    """
    rn = randint(0, 1000000)

    pc = [
        {"id": "t_rast_mapcalc_%i" % rn,
         "module": "t.rast.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = float((%(nir)s - %(red)s)/"
                              "(%(nir)s + %(red)s))" % {"result": output_time_series,
                                                        "nir": nir_time_series,
                                                        "red": red_time_series}},
                    {"param": "inputs",
                     "value": "%(nir)s,%(red)s"%{"nir": nir_time_series,
                                                 "red": red_time_series}},
                    {"param": "basename",
                     "value": "ndvi"},
                    {"param": "output",
                     "value": output_time_series}]},
        {"id": "t_rast_color_%i" % rn,
         "module": "t.rast.colors",
         "inputs": [{"param": "input",
                     "value": output_time_series},
                    {"param": "color",
                     "value": "ndvi"}]}]

    return pc


def get_process_list(args):
    """Analyse the process description and return the GRaaS process chain and the name of the processing result

    :param args: The process description arguments
    :return: (output_time_series, pc)
    """

    input_names, process_list = process_definitions.analyse_process_graph(args)

    # Two input names are required
    if len(input_names) != 2:
        raise Exception("Two input time series are required")

    # Create the output name based on the input name and method
    output_time_series = input_names[0].split("@")[0] + "_" + PROCESS_NAME

    nir_time_series = None
    red_time_series = None

    for input_name in input_names:
        if "nir" in args and args["nir"] in input_name:
            nir_time_series = input_name
        if "red" in args and args["red"] in input_name:
            red_time_series = input_name

    if nir_time_series is None or red_time_series is None:
        raise Exception("Band information is missing from process description")

    pc = create_graas_process_chain_entry(nir_time_series, red_time_series, output_time_series)
    process_list.extend(pc)

    return [output_time_series,], process_list


process_definitions.PROCESS_DICT[PROCESS_NAME] = get_process_list
