# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import Node, check_node_parents
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "apply_mask"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or a space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)

    p_mask = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or a space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)

    rv = ReturnValue(description="Masked EO data.",
                     schema={"type": "object", "format": "eodata"})

    # Example
    arguments = {
                "data": {"from_node": "get_strds_data"},
                "mask": {"from_node": "get_mask_data"},
            }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"apply_mask_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Applies a mask to an EO dataset. "
                                        "Each pixel that is 0 or nodata in the mask is set to nodata. "
                                        "See also multilayer_mask.",
                            summary="Apply a mask to an EO dataset.",
                            parameters={"data": p_data, "mask": p_mask},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_name, mask_name, output_name):
    """Create a Actinia process description that uses r.mapcalc 
       to apply a mask.
       
       NOTE: according to multilayer_mask, 0 means not masked, 1 means masked
             this is the other way around compared to GRASS

    :param input_name: The input map name
    :param mask_name: The mask map name
    :param output_name: The name of the output map
    :return: A Actinia process chain description
    """
    input_name = ActiniaInterface.layer_def_to_grass_map_name(input_name)
    mask_name = ActiniaInterface.layer_def_to_grass_map_name(mask_name)
    
    rn = randint(0, 1000000)

    pc = {"id": "r_mapcalc_%i" % rn,
         "module": "r.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = if(isnull(%(mask)s) || %(mask)s == 0, "
                              "null(), %(raw)s)" % {"result": output_name,
                                                    "raw": input_name,
                                                    "mask": mask_name}}
                   ]}

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

    if "mask" not in node.arguments:
        raise Exception("Parameter mask is required.")

    nmasks = len(node.get_parent_by_name("mask").output_names)
    ninputs = len(node.get_parent_by_name("data").output_names)

    if nmasks > 1 and nmasks != ninputs:
        raise Exception("Either a single mask or a separate mask for each layer is required.")

    mask_name = None
    if nmasks == 1:
        mask_name = node.get_parent_by_name("mask").output_names[0]

    for i in range(len(node.get_parent_by_name("data").output_names)):
        input_name = node.get_parent_by_name("data").output_names[i]
        if nmasks > 1:
            mask_name = node.get_parent_by_name("mask").output_names[i]
        location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
        output_name = "%s_%s" % (layer_name, PROCESS_NAME)
        output_names.append(output_name)
        node.add_output(output_name=output_name)

        pc = create_process_chain_entry(input_name, mask_name, output_name)
        process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
