# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import Node, check_node_parents
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "resample"


def create_process_description():

    # see https://github.com/Open-EO/openeo-processes/blob/master/resample_cube_spatial.json

    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)
    p_target = Parameter(description="Any openEO process object that returns a raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)
    p_method = Parameter(description="The resampling method to use",
                         schema={"type": "string"},
                         required=True)

    p_method.enum = ["near",
                     "bilinear",
                     "cubic",
                     "lanczos",
                     "average",
                     "mode",
                     "max",
                     "min",
                     "med",
                     "q1",
                     "q3"
                ]

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    simple_example = {
        "resample_1": {
            "process_id": PROCESS_NAME,
            "arguments": {
                "data": {"from_node": "get_strds_data_1"},
                "target": {"from_node": "get_data_2"},
                "method": "average",
            }
        }
    }

    examples = dict(simple_example=simple_example)

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Change the resolution of a space-time raster dataset "
                                        "with different methods.",
                            summary="Spatially resample a space-time raster dataset.",
                            parameters={"imagery": p_data, "target": p_target, "method": p_method},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_name, target_name, method, output_name):
    """Create a Actinia process description.

    :param input_name: The input time series name
    :param target_name: The input target raster name
    :param method: The method for time reduction
    :param output_map: The name of the output raster map
    :return: A Actinia process chain description
    """
    input_name = ActiniaInterface.layer_def_to_grass_map_name(input_name)

    rn = randint(0, 1000000)



    # TODO: a new GRASS addon that
    # 1. fetches a list of raster maps in a strds
    # 2. resamples each raster map with the selected method
    

    pc = [
         {"id": "t_rast_series_%i" % rn,
          "module": "t.rast.series",
          "inputs": [{"param": "input", "value": input_name},
                     {"param": "method", "value": method},
                     {"param": "output", "value": output_name}],
          "flags": "t"}
          ]

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain
    and the name of the processing result layer
    which is a single raster layer

    :param node: The process node
    :return: (output_names, actinia_process_list)
    """

    input_names, process_list = check_node_parents(node=node)
    output_names = []

    if "method" not in node.arguments:
        raise Exception("Parameter method is required.")

    for input_name in node.get_parent_by_name("data").output_names:
        # multiple strds as input ?
        # multiple raster layers as output !
        location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
        output_name = "%s_%s" % (layer_name, PROCESS_NAME)
        output_names.append(output_name)
        node.add_output(output_name=output_name)

        pc = create_process_chain_entry(input_name, node.arguments["method"], output_name)
        process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
