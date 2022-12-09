# -*- coding: utf-8 -*-
import json
from random import randint

from openeo_grass_gis_driver.actinia_processing.base import (
    check_node_parents,
    DataObject,
    GrassDataType,
    create_output_name,
)
from openeo_grass_gis_driver.models.process_graph_schemas import (
    ProcessGraphNode,
    ProcessGraph,
)
from openeo_grass_gis_driver.models.process_schemas import (
    Parameter,
    ProcessDescription,
    ReturnValue,
    ProcessExample,
)
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
        schema={"type": "object", "subtype": "raster-cube"},
        optional=False,
    )
    p_poly = Parameter(
        description="One or more polygons used for filtering",
        schema={
            "anyOf": [
                {"type": "object", "subtype": "geojson"},
                {"type": "object", "subtype": "vector-cube"},
            ]
        },
        optional=False,
    )
    p_value = Parameter(
        description="The value used to replace non-zero and `true` values with",
        schema={"type": "object", "subtype": "string"},
        optional=True,
    )
    p_inside = Parameter(
        description="If set to `true` all pixels for which the point at the pixel center "
        "**does** intersect with any polygon are replaced",
        schema={"type": "boolean"},
        optional=True,
    )

    rv = ReturnValue(
        description="Processed EO data.",
        schema={"type": "object", "subtype": "raster-cube"},
    )

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
        process_graph={"filter_polygon_1": node},
    )
    examples = [
        ProcessExample(
            title="Simple example", description="Simple example", process_graph=graph
        )
    ]

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
            "inside": p_inside,
        },
        returns=rv,
        examples=examples,
    )

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(
    input_object: DataObject,
    vector_object,
    mask_value,
    inside,
    output_object: DataObject,
):
    """Create a Actinia command of the process chain

    :param input_object:
    :param vector_object:
    :return: A Actinia process chain description
    """

    # TODO: support geojson as input

    rn = randint(0, 1000000)
    pc = []

    importer = {
        "id": "v_in_geojson_%i" % rn,
        "module": "v.in.geojson",
        "inputs": [
            {"param": "input", "value": json.dumps(vector_object)},
            {"param": "output", "value": "geojson_mask"},
        ],
    }

    mask_dict = {
        "id": "r_mask_%i" % rn,
        "module": "r.mask",
        "inputs": [{"param": "raster", "value": "polymask"}],
    }
    if inside is True:
        mask_dict["flags"] = "i"

    create_mask = [
        {
            "id": "v_to_rast_%i" % rn,
            "module": "v.to.rast",
            "inputs": [
                {"param": "input", "value": "geojson_mask"},
                {"param": "output", "value": "polymask"},
                {"param": "type", "value": "area"},
                {"param": "use", "value": "val"},
            ],
        },
        mask_dict,
    ]

    # replace all pixels where mask is null
    if mask_value is None or mask_value == "null":
        mask_value = "null()"

    do_mask = {
        "id": "t_rast_mapcalc_%i" % rn,
        "module": "t.rast.mapcalc",
        "inputs": [
            {
                "param": "expression",
                "value": "%(result)s = if(isnull(%(inmap)s), %(maskval)s, %(inmap)s)"
                % {
                    "result": output_object.name,
                    "inmap": input_object.grass_name(),
                    "maskval": str(mask_value),
                },
            },
            {"param": "inputs", "value": input_object.grass_name()},
            {"param": "basename", "value": output_object.name},
            {"param": "output", "value": output_object.name},
        ],
    }

    remove_maps = [
        {
            "id": "g_remove_rast_%i" % rn,
            "module": "g.remove",
            "inputs": [
                {"param": "type", "value": "raster"},
                {"param": "name", "value": "MASK,polymask"},
            ],
            "flags": "f",
        },
        {
            "id": "g_remove_vect_%i" % rn,
            "module": "g.remove",
            "inputs": [
                {"param": "type", "value": "vector"},
                {"param": "name", "value": "geojson_mask"},
            ],
            "flags": "f",
        },
    ]

    output_info = {
        "id": "t_info_%i" % rn,
        "module": "t.info",
        "inputs": [
            {"param": "input", "value": output_object.grass_name()},
            {"param": "type", "value": "strds"},
        ],
        "flags": "g",
    }

    pc.append(importer)
    pc.extend(create_mask)
    pc.append(do_mask)
    pc.extend(remove_maps)
    pc.append(output_info)

    return pc


def get_process_list(node: Node):
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "data" not in node.arguments or "mask" not in node.arguments:
        raise Exception("Process %s requires parameter data, polygons" % PROCESS_NAME)

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
        name=create_output_name(input_object.name, node), datatype=GrassDataType.STRDS
    )
    output_objects.append(output_object)
    node.add_output(output_object=output_object)

    pc = create_process_chain_entry(
        input_object, vector_object, mask_value, inside, output_object
    )
    process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
