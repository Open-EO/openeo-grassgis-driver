# -*- coding: utf-8 -*-
import json
from random import randint

from openeo_grass_gis_driver.actinia_processing.base import check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from .base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "filter_spatial"


def create_process_description():
    p_data = Parameter(
        description="Any openEO process object that returns raster datasets "
        "or space-time raster dataset",
        schema={
            "type": "object",
            "subtype": "raster-cube"},
        optional=False)
    p_poly = Parameter(description="One or more polygons used for filtering",
                       schema={"anyOf": [
                           {
                               "type": "object",
                               "subtype": "geojson"
                           },
                           {
                               "type": "object",
                               "subtype": "vector-cube"
                           }]},
                       optional=False)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "data": {"from_node": "get_data_1"},
        "polygons": {"from_node": "get_data_2"},
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "filter_polygon_1": node})
    examples = [
        ProcessExample(
            title="Simple example",
            description="Simple example",
            process_graph=graph)]

    pd = ProcessDescription(
        id=PROCESS_NAME,
        description="Limits the data cube over the spatial dimensions to the specified polygons.\n\nThe filter retains "
        "a pixel in the data cube if the point at the pixel center intersects with at least one of the polygons (as  "
        "defined in the Simple Features standard by the OGC).",
        summary="Spatial filter using polygons",
        parameters={
            "data": p_data,
            "geometries": p_poly},
        returns=rv,
        examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object: DataObject, vector_object,
                               output_object: DataObject):
    """Create a Actinia command of the process chain

    :param input_object:
    :param vector_object:
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    pc = [{"id": "v_in_geojson_%i" % rn,
           "module": "v.in.geojson",
           "inputs": [{"param": "input",
                       "value": vector_object},
                      {"param": "output",
                       "value": "geojson_mask"},
                      ]},
          {"id": "v_to_rast_%i" % rn,
          "module": "v.to.rast",
           "inputs": [{"param": "input", "value": "geojson_mask"},
                      {"param": "output", "value": "MASK"},
                      {"param": "type", "value": "point,line,area"},
                      {"param": "use", "value": "val"},
                      ]},
          {"id": "t_rast_algebra_%i" % rn,
           "module": "t.rast.algebra",
           "inputs": [{"param": "expression",
                       "value": "%(result)s = 1 * %(input)s" %
                       {"result": output_object.grass_name(),
                        "input": input_object.grass_name()}},
                      {"param": "basename",
                       "value": "filter_polygon"},
                      ]},
          {"id": "r_mask_%i" % rn,
           "module": "r_mask",
           "inputs": {"flags": "r"}}
          ]

    return pc


def get_process_list(node: Node):
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "data" not in node.arguments or \
            "polygons" not in node.arguments:
        raise Exception(
            "Process %s requires parameter data, polygons" %
            PROCESS_NAME)

    input_objects = node.get_parent_by_name(parent_name="data").output_objects
    vector_objects = node.arguments["polygons"]

    if not input_objects:
        raise Exception("Process %s requires an input strds" % PROCESS_NAME)

    if not vector_objects:
        raise Exception("Process %s requires an input vector" % PROCESS_NAME)

    input_object = list(input_objects)[-1]

    output_object = DataObject(
        name=f"{input_object.name}_{PROCESS_NAME}",
        datatype=GrassDataType.STRDS)
    output_objects.append(output_object)

    pc = create_process_chain_entry(input_object, vector_object, output_object)
    process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
