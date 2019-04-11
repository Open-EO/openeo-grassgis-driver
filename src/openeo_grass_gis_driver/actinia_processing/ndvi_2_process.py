# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.process_schemas import Parameter, ProcessDescription, ReturnValue
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "NDVI2"


def create_process_description():

    p_red = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                                  "that contains the RED band for NDVI computation.",
                       schema={"type": "object", "format": "eodata"},
                      required=True)

    p_nir = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                                  "that contains the NIR band for NDVI computation.",
                      schema={"type": "object", "format": "eodata"},
                      required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    simple_example = {
            "process_id": PROCESS_NAME,
            "red": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.landsat.strds.lsat5_red"
            },
            "nir": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.landsat.strds.lsat5_nir"
            }
        }

    examples = dict(simple_example=simple_example)

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Compute the NDVI based on the red and nir bands of the input datasets.",
                            summary="Compute the NDVI based on the red and nir bands of the input datasets.",
                            parameters={"red": p_red, "nir": p_nir},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


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
    process_list = []

    # First analyse the data entries
    if "red" not in process:
        raise Exception("Process %s requires parameter <red>" % PROCESS_NAME)

    if "nir" not in process:
        raise Exception("Process %s requires parameter <nir>" % PROCESS_NAME)

    # Get the red and ir data separately
    red_process = dict(myproc="myproc", red=process["red"])
    nir_process = dict(myproc="myproc", red=process["nir"])

    red_input_names, red_process_list = process_node_to_actinia_process_chain(red_process)
    process_list.extend(red_process_list)
    nir_input_names, nir_process_list = process_node_to_actinia_process_chain(nir_process)
    process_list.extend(nir_process_list)

    if not red_input_names:
        raise Exception("Process %s requires an input strds for band <red>" % PROCESS_NAME)

    if not nir_input_names:
        raise Exception("Process %s requires an input strds for band <nir>" % PROCESS_NAME)

    red_stds = red_input_names[-1]
    nir_strds = nir_input_names[-1]

    # Take the last entry from the
    if len(red_input_names) > 1:
        output_names.extend(red_input_names[0:-1])

    # Take the last entry from the
    if len(nir_input_names) > 1:
        output_names.extend(nir_input_names[0:-1])

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(red_stds)
    output_name = "%s_%s" % (layer_name, PROCESS_NAME)
    output_names.append(output_name)

    pc = create_process_chain_entry(nir_strds, red_stds, output_name)
    process_list.extend(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
