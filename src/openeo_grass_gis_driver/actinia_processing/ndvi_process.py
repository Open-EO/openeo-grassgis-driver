# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, check_node_parents
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "NDVI"


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
        "ndvi_1": {
            "process_id": PROCESS_NAME,
            "arguments": {
                "red": {"from_node": "get_red_data"},
                "nir": {"from_node": "get_nir_data"},
            }
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
    """Create a Actinia process description that uses t.rast.mapcalc to create the NDVI time series

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


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_names, actinia_process_list)
    """

    input_names, process_list = check_node_parents(node=node)
    output_names = []

    # First analyse the data entries
    if "red" not in node.arguments:
        raise Exception("Process %s requires parameter <red>" % PROCESS_NAME)

    if "nir" not in node.arguments:
        raise Exception("Process %s requires parameter <nir>" % PROCESS_NAME)

    # Get the red and nir data separately
    red_input_names = node.get_parent_by_name(parent_name="red").output_names
    nir_input_names = node.get_parent_by_name(parent_name="nir").output_names

    if not red_input_names:
        raise Exception("Process %s requires an input strds for band <red>" % PROCESS_NAME)

    if not nir_input_names:
        raise Exception("Process %s requires an input strds for band <nir>" % PROCESS_NAME)

    red_stds = list(red_input_names)[-1]
    nir_strds = list(nir_input_names)[-1]

    output_names.extend(list(red_input_names))
    output_names.extend(list(nir_input_names))

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(red_stds)
    output_name = "%s_%s" % (layer_name, PROCESS_NAME)
    output_names.append(output_name)
    node.add_output(output_name=output_name)

    pc = create_process_chain_entry(nir_strds, red_stds, output_name)
    process_list.extend(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
