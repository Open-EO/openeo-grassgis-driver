# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph, ProcessGraphNode

from openeo_grass_gis_driver.actinia_processing.base import Node, check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

from flask import make_response, jsonify, request

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

# not in the official list
PROCESS_NAME = "multilayer_mask"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or a space-time raster dataset",
                       schema={"type": "object", "subtype": "raster-cube"},
                       required=True)

    rv = ReturnValue(description="Multilayer mask as EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {"data": {"from_node": "get_strds_data"}}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"multilayer_mask_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Creates a mask using several bands of an EO dataset. "
                                        "Each pixel that has nodata or invalid value in any of "
                                        "the layers/bands gets value 1, pixels that have valid "
                                        "values in all layers/bands get value 0.",
                            summary="Create a multilayer mask from several raster datasets.",
                            parameters={"data": p_data},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(data_object: DataObject, output_object: DataObject):
    """Create a Actinia process description that uses t.rast.series
       and r.mapcalc to create a multilayer mask.

    :param data_object: The input time series object
    :param output_object: The name of the output raster map
    :return: A Actinia process chain description
    """

    output_temp_object = DataObject(name=f"{output_object.name}_temp", datatype=GrassDataType.RASTER)

    # get number of maps in input_time_series
    iface = ActiniaInterface()
    # this is not working because the input object might not yet exist
    status_code, layer_data = iface.layer_info(layer_name=data_object.grass_name())
    if status_code != 200:
        return make_response(jsonify({"description": "An internal error occurred "
                                                     "while catching GRASS GIS layer information "
                                                     "for layer <%s>!\n Error: %s"
                                                     "" % (data_object, str(layer_data))}, 400))
    nmaps = layer_data['number_of_maps']

    rn = randint(0, 1000000)

    pc = [
        {"id": "t_rast_series_%i" % rn,
         "module": "t.rast.series",
         "inputs": [{"param": "input", "value": data_object.grass_name()},
                    {"param": "method", "value": "count"},
                    {"param": "output", "value": output_temp_object.grass_name()}],
         "flags": "t"},

        {"id": "r_mapcalc_%i" % rn,
         "module": "r.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = int(if(%(raw)s < %(nmaps)s, 1, 0))" %
                              {"result": output_object.grass_name(),
                               "raw": output_temp_object.grass_name(),
                               "nmaps": str(nmaps)}}
                    ],
         }]
    # g.remove raster name=output_name_tmp -f ?

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain
    and the name of the processing result layer
    which is a single raster layer

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    data_object = list(input_objects)[-1]
    output_object = DataObject(name=f"{data_object.name}_{PROCESS_NAME}", datatype=GrassDataType.RASTER)
    output_objects.append(output_object)
    node.add_output(output_object=output_object)

    pc = create_process_chain_entry(data_object, output_object)
    process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
