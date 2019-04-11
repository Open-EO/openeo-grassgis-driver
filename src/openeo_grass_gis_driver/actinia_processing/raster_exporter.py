# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "raster_exporter"


def create_process_description():
    p_imagery = Parameter(description="Any openEO process object that returns raster datasets "
                                      "or space-time raster dataset",
                          schema={"type": "object", "format": "eodata"},
                          required=True)
    p_format = Parameter(description="The format of the export. Default is GeotTiff format.",
                         schema={"type": "string", "default": "GTiff"},
                         required=False)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    simple_example = {
        "process_id": PROCESS_NAME,
        "format": "GTiff",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.landsat.raster.elevation",
            "imagery": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.landsat.raster.slope"
            }
        }
    }

    examples = dict(simple_example=simple_example)

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="This process exports an arbitrary number of raster map layers "
                                        "using the region specified upstream.",
                            summary="Exports raster map layers using the region specified upstream.",
                            parameters={"imagery": p_imagery, "format": p_format},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_name):
    """Create a Actinia command of the process chain that computes the regional statistics based on a
    strds and a polygon.

    :param input_name: The name of the raster layer
    :return: A Actinia process chain description
    """

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
    input_name = layer_name
    if mapset is not None:
        input_name = layer_name + "@" + mapset

    rn = randint(0, 1000000)
    pc = []

    exporter = {
        "id": "exporter_%i" % rn,
        "module": "exporter",
        "outputs": [{"export": {"type": "raster", "format": "GTiff"},
                     "param": "map",
                     "value": input_name}]}

    pc.append(exporter)

    return pc


def get_process_list(args):
    """Analyse the process description and return the Actinia process chain and the name of the processing result layer
    which is a single raster layer

    :param args: The process description
    :return: (output_names, actinia_process_list)
    """

    # Get the input description and the process chain to attach this process
    input_names, process_list = process_node_to_actinia_process_chain(args)
    output_names = []

    # Pipe the inputs to the outputs
    for input_name in input_names:
        output_name = input_name
        output_names.append(output_name)

        pc = create_process_chain_entry(input_name=input_name)
        process_list.extend(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
