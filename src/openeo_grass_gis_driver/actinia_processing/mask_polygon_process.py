# -*- coding: utf-8 -*-
import json
from random import randint

from openeo_grass_gis_driver.actinia_processing.base import \
     check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_graph_schemas import \
     ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import \
     Parameter, ProcessDescription, ReturnValue, ProcessExample
from .base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "mask_polygon"


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
    p_value = Parameter(
        description="The value used to replace non-zero and `true` values with",
        schema={
            "type": "object",
            "subtype": "string"},
        optional=True)
    p_inside = Parameter(
        description="If set to `true` all pixels for which the point at the pixel center "
        "**does** intersect with any polygon are replaced",
        schema={
            "type": "boolean"},
        optional=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "data": {"from_node": "get_data_1"},
        "mask": "some geojson",
                "replacement": "null",
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
            "mask": p_poly,
            "replacement": p_value,
            "inside": p_inside},
        returns=rv,
        examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object: DataObject, vector_object,
                               mask_value, inside, output_object: DataObject):
    """Create a Actinia command of the process chain

    :param input_object:
    :param vector_object:
    :return: A Actinia process chain description
    """

    # TODO: support geojson as input

    rn = randint(0, 1000000)
    pc = []

    importer = {"id": "v_in_geojson_%i" % rn,
                "module": "v.in.geojson",
                "inputs": [{"param": "input",
                            "value": vector_object},
                           {"param": "output",
                            "value": "geojson_mask"},
                           ]}

    if inside is False:
        create_mask = {"id": "v_to_rast_%i" % rn,
                       "module": "v.to.rast",
                       "inputs": [{"param": "input", "value": "geojson_mask"},
                                  {"param": "output", "value": "polymask"},
                                  {"param": "type", "value": "area"},
                                  {"param": "use", "value": "val"},
                                  ]}
    else:
        create_mask = [{"id": "v_to_rast_%i" % rn,
                        "module": "v.to.rast",
                        "inputs": [{"param": "input", "value": "geojson_mask"},
                                   {"param": "output", "value": "polymask_inv"},
                                   {"param": "type", "value": "area"},
                                   {"param": "use", "value": "val"},
                                   ]},
                       {"id": "r:mapcalc_%i" % rn,
                        "module": "r.mapcalc",
                        "inputs": [{"param": "expression",
                                    "value": "polymask = if(isnull(polymask_inv), 1, null())"}
                                   ]}]

    # replace all pixels where mask is null
    if mask_value == "null":
        do_mask = {"id": "t_rast_mapcalc_%i" % rn,
                   "module": "t.rast.mapcalc",
                   "inputs": [{"param": "expression",
                               "value": "%(result)s = if(isnull(%(mask_name)s), "
                               "%(raw)s, null())" % {"result": output_object.grass_name(),
                                                     "mask_name": "polymask",
                                                     "raw": input_object.grass_name()}},
                              {"param": "basename",
                               "value": "masked"},
                              {"param": "output",
                               "value": output_object.grass_name()},
                              ]}
    else:
        do_mask = {"id": "t_rast_mapcalc_%i" % rn,
                   "module": "t.rast.mapcalc",
                   "inputs": [{"param": "expression",
                               "value": "%(result)s = if(isnull(%(mask_name)s), "
                               "%(raw)s, %(mask_value)s)" % {"result": output_object.grass_name(),
                                                             "mask_name": "polymask",
                                                             "raw": input_object.grass_name(),
                                                             "mask_value": mask_value}},
                              {"param": "basename",
                               "value": "masked"},
                              {"param": "output",
                               "value": output_object.grass_name()},
                              ]}

    pc.append(importer)
    pc.append(create_mask)
    pc.append(do_mask)

    return pc


def get_process_list(node: Node):
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "data" not in node.arguments or \
            "mask" not in node.arguments:
        raise Exception(
            "Process %s requires parameter data, polygons" %
            PROCESS_NAME)

    if "replacement" in node.arguments:
        mask_value = node.arguments["replacement"]
    else:
        mask_value = "null"

    inside = False
    if "inside" in node.arguments:
        if node.arguments["inside"] == "true":
            inside = True

    input_objects = node.get_parent_by_name(parent_name="data").output_objects
    vector_object = node.arguments["mask"]

    if not input_objects:
        raise Exception("Process %s requires an input strds" % PROCESS_NAME)

    input_object = list(input_objects)[-1]

    output_object = DataObject(
        name=f"{input_object.name}_{PROCESS_NAME}",
        datatype=GrassDataType.STRDS)
    output_objects.append(output_object)

    pc = create_process_chain_entry(
        input_object, vector_object, mask_value, inside, output_object)
    process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
