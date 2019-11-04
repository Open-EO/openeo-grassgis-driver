# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph, ProcessGraphNode

from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
    check_node_parents, DataObject
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2019, Markus Metz, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "load_collection"

# based on get_data, updated to OpenEO API v0.4

def create_process_description():

    p_data = Parameter(description="The identifier of a single raster-, vector- or space-time raster dataset",
                        schema={"type": "string",
                                  "examples": ["nc_spm_08.landsat.raster.lsat5_1987_10",
                                               "nc_spm_08.PERMANENT.vector.lakes",
                                               "ECAD.PERMANENT.strds.temperature_1950_2017_yearly"]},
                          required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    # Example
    arguments = {"id": "latlong_wgs84.modis_ndvi_global.strds.ndvi_16_5600m"}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"load_strds_collection": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="This process returns a raster-, a vector- or a space-time raster "
                                        "datasets that is available in the /collections endpoint.",
                            summary="Returns a single dataset that is available in "
                                    "the /collections endpoint for processing",
                            parameters={"id": p_data},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()



def create_process_chain_entry(input_object: DataObject):
    """Create a Actinia process description that r.info, v.info, or t.info.

    :param input_object: The input object name
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    pc = {}

    if input_object.is_raster():
        pc = {"id": "r_info_%i" % rn,
              "module": "r.info",
              "inputs": [{"param": "map", "value": input_object.grass_name()}, ],
              "flags": "g"}
    elif input_object.is_vector():
        pc = {"id": "v_info_%i" % rn,
              "module": "v.info",
              "inputs": [{"param": "map", "value": input_object.grass_name()}, ],
              "flags": "g"}
    elif input_object.is_strds():
        pc = {"id": "t_info_%i" % rn,
              "module": "t.info",
              "inputs": [{"param": "input", "value": input_object.grass_name()}, ],
              "flags": "g"}
    else:
        raise Exception("Unsupported datatype")

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    # First analyse the data entry
    if "id" not in node.arguments:
        raise Exception("Process %s requires parameter <data>" % PROCESS_NAME)

    output_object = DataObject.from_string(node.arguments["id"])
    output_objects.append(output_object)
    node.add_output(output_object)

    pc = create_process_chain_entry(input_object=output_object)
    process_list.append(pc)

    for input_object in input_objects:
        output_objects.append(input_object)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
