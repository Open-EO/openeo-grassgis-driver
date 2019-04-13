# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.process_schemas import Parameter, ProcessDescription, ReturnValue
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "get_data"


def create_process_description():
    p_imagery = Parameter(description="Any openEO process object that returns raster datasets "
                                      "or space-time raster dataset",
                          schema={"type": "object", "format": "eodata"},
                          required=False)

    p_data_id = Parameter(description="The identifier of a single raster-, vector- or space-time raster dataset",
                          schema={"type": "string",
                                  "examples": ["nc_spm_08.landsat.raster.lsat5_1987_10",
                                               "nc_spm_08.PERMANENT.vector.lakes",
                                               "ECAD.PERMANENT.strds.temperature_1950_2017_yearly"]},
                          required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    simple_example = {
        "process_id": PROCESS_NAME,
        "data_id": "nc_spm_08.PERMANENT.vector.lakes",
    }
    raster_vector_example = {
        "process_id": PROCESS_NAME,
        "data_id": "nc_spm_08.landsat.raster.lsat5_1987_10",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.PERMANENT.vector.lakes"
        }
    }
    strds_example = {
        "process_id": PROCESS_NAME,
        "data_id": "ECAD.PERMANENT.strds.temperature_1950_2017_yearly",
        "imagery": {
            "process_id": "get_data",
            "data_id": "ECAD.PERMANENT.strds.precipitation_1950_2017_yearly"
        }
    }

    examples = dict(simple_example=simple_example,
                    raster_vector_example=raster_vector_example,
                    strds_example=strds_example)

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="This process returns a raster-, a vector- or a space-time raster "
                                        "datasets that is available in the /collections endpoint.",
                            summary="Returns a single dataset that is available in "
                                    "the /collections endpoint for processing",
                            parameters={"imagery": p_imagery, "data_id": p_data_id},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_name):
    """Create a Actinia process description that uses t.rast.series to create the minimum
    value of the time series.

    :param input_time_series: The input time series name
    :param output_map: The name of the output map
    :return: A Actinia process chain description
    """

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
    input_name = layer_name
    if mapset is not None:
        input_name = layer_name + "@" + mapset

    rn = randint(0, 1000000)

    pc = {}

    if datatype == "raster":
        pc = {"id": "r_info_%i" % rn,
              "module": "r.info",
              "inputs": [{"param": "map", "value": input_name}, ],
              "flags": "g"}
    elif datatype == "vector":
        pc = {"id": "v_info_%i" % rn,
              "module": "v.info",
              "inputs": [{"param": "map", "value": input_name}, ],
              "flags": "g"}
    elif datatype == "strds":
        pc = {"id": "t_info_%i" % rn,
              "module": "t.info",
              "inputs": [{"param": "input", "value": input_name}, ],
              "flags": "g"}
    else:
        raise Exception("Unsupported datatype")

    return pc


def get_process_list(process):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param process: The process description
    :return: (output_names, actinia_process_list)
    """

    input_names, process_list = process_node_to_actinia_process_chain(process)
    output_names = []

    # First analyse the data entrie
    if "data_id" not in process:
        raise Exception("Process %s requires parameter <data_id>" % PROCESS_NAME)

    output_names.append(process["data_id"])

    pc = create_process_chain_entry(input_name=process["data_id"])
    process_list.append(pc)

    # Then add the input to the output
    for input_name in input_names:
        # Create the output name based on the input name and method
        output_name = input_name
        output_names.append(output_name)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
