# -*- coding: utf-8 -*-
from random import randint
import json
from .base import analyse_process_graph, PROCESS_DICT_LEGACY, PROCESS_DESCRIPTION_DICT_LEGACY
from openeo_grass_gis_driver.process_schemas import Parameter, ProcessDescription, ReturnValue
from .actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "NDVI"


def create_process_description():

    p_imagery = Parameter(description="Any openEO process object that returns space-time raster dataset",
                          schema={"type": "object", "format": "eodata"},
                          required=False)

    p_red = Parameter(description="A substring a space-time raster dataset identifer "
                                  "that contains the RED band for NDVI computation.",
                      schema={"type": "string", "examples": {"red": "lsat5_red"}},
                      required=True)

    p_nir = Parameter(description="A substring a space-time raster dataset identifer "
                                  "that contains the NIR band for NDVI computation.",
                      schema={"type": "string", "examples": {"red": "lsat5_nir"}},
                      required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    simple_example = {
            "process_id": PROCESS_NAME,
            "red": "lsat5_red",
            "nir": "lsat5_nir",
            "imagery": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.landsat.strds.lsat5_red",
                "imagery": {
                    "process_id": "get_data",
                    "data_id": "nc_spm_08.landsat.strds.lsat5_nir"
                }
            }
        }

    examples = dict(simple_example=simple_example)

    pd = ProcessDescription(name=PROCESS_NAME,
                            description="Compute the NDVI based on the red and nir bands of the input datasets.",
                            summary="Compute the NDVI based on the red and nir bands of the input datasets.",
                            parameters={"imagery":p_imagery, "red": p_red, "nir": p_nir},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT_LEGACY[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(nir_time_series, red_time_series, output_time_series):
    """Create a Actinia process description that uses t.rast.series to create the minimum
    value of the time series.

    :param nir_time_series: The NIR band time series name
    :param red_time_series: The RED band time series name
    :param output_time_series: The name of the output time series
    :return: A list of Actinia process chain descriptions
    """
    nir_time_series = ActiniaInterface.layer_def_to_grass_map_name(nir_time_series)
    red_time_series = ActiniaInterface.layer_def_to_grass_map_name(red_time_series)
    output_name = ActiniaInterface.layer_def_to_grass_map_name(output_time_series)

    rn = randint(0, 1000000)

    pc = [
        {"id": "t_rast_mapcalc_%i" % rn,
         "module": "t.rast.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = float((%(nir)s - %(red)s)/"
                              "(%(nir)s + %(red)s))" % {"result": output_name,
                                                        "nir": nir_time_series,
                                                        "red": red_time_series}},
                    {"param": "inputs",
                     "value": "%(nir)s,%(red)s" % {"nir": nir_time_series,
                                                   "red": red_time_series}},
                    {"param": "basename",
                     "value": "ndvi"},
                    {"param": "output",
                     "value": output_name}]},
        {"id": "t_rast_color_%i" % rn,
         "module": "t.rast.colors",
         "inputs": [{"param": "input",
                     "value": output_name},
                    {"param": "color",
                     "value": "ndvi"}]}]

    return pc


def get_process_list(process):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param args: The process description arguments
    :return: (output_names, actinia_process_list)
    """
    output_names = []

    # First analyse the data entries
    if "red" not in process:
        raise Exception("Process %s requires parameter <red>" % PROCESS_NAME)

    if "nir" not in process:
        raise Exception("Process %s requires parameter <nir>" % PROCESS_NAME)

    red_strds = None
    nir_strds = None
    input_names, process_list = analyse_process_graph(process)

    # Find the red and nir datasets in the input
    for input_name in input_names:
        if process["red"] in input_name:
            red_strds = input_name
        elif process["nir"] in input_name:
            nir_strds = input_name
        else:
            # Pipe other inputs to the output
            output_names.append(input_name)

    if not red_strds:
        raise Exception("Process %s requires an input strds for band <red>" % PROCESS_NAME)

    if not nir_strds:
        raise Exception("Process %s requires an input strds for band <nir>" % PROCESS_NAME)

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(red_strds)
    output_name = "%s_%s" % (layer_name, PROCESS_NAME)
    output_names.append(output_name)

    pc = create_process_chain_entry(nir_strds, red_strds, output_name)
    process_list.extend(pc)

    return output_names, process_list


PROCESS_DICT_LEGACY[PROCESS_NAME] = get_process_list
