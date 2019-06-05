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

PROCESS_NAME = "multilayer_mask"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or a space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)

    rv = ReturnValue(description="Multilayer mask as EO data.",
                     schema={"type": "object", "format": "eodata"})

    simple_example = {
        "multilayer_mask_1": {
            "process_id": PROCESS_NAME,
            "arguments": {
                "data": {"from_node": "get_strds_data"},
            }
        }
    }

    examples = dict(simple_example=simple_example)

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Creates a mask using several bands of an EO dataset. "
                                        "Each pixel that has nodata or invalid value in any of "
					"the layers/bands gets value 1, pixels that have valid "
					"values in all layers/bands get value 0.",
                            summary="Create a multilayer mask from several raster datasets.",
                            parameters={"imagery": p_data},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_time_series, output_name):
    """Create a Actinia process description that uses t.rast.series 
       and r.mapcalc to create a multilayer mask.

    :param input_time_series: The input time series name
    :param output_name: The name of the output map
    :return: A Actinia process chain description
    """
    input_name = ActiniaInterface.layer_def_to_grass_map_name(input_time_series)
    output_name_tmp = output_name + '_tmp'
    
    # TODO: get number of maps in input_name
    nmaps = ??? # Number of registered maps

    rn = randint(0, 1000000)

    pc = {"id": "t_rast_series_%i" % rn,
          "module": "t.rast.series",
          "inputs": [{"param": "input", "value": input_name},
                     {"param": "method", "value": "count"},
                     {"param": "output", "value": output_name_tmp}],
          "flags": "t",

          "module": "r.mapcalc",
          "inputs": [{"param": "expression",
                     "value": "%(result)s = int(if(%(raw)s < %(nmaps)s, 1, 0))" % 
                                            {"result": output_name,
                                             "raw": input_name,
                                             "nmaps": str(nmaps)}},
                    {"param": "output",
                     "value": output_name}],
	  }
	  # g.remove raster name=output_name_tmp -f ?

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
        location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
        output_name = "%s_%s" % (layer_name, PROCESS_NAME)
        output_names.append(output_name)
        node.add_output(output_name=output_name)

        pc = create_process_chain_entry(input_name, node.arguments["method"], output_name)
        process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
