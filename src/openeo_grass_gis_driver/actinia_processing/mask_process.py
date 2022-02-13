# -*- coding: utf-8 -*-
import json
from random import randint
from typing import Tuple

from openeo_grass_gis_driver.models.process_graph_schemas import \
     ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import \
     check_node_parents, DataObject, GrassDataType, \
     create_output_name
from openeo_grass_gis_driver.models.process_schemas import \
     Parameter, ProcessDescription, ReturnValue, ProcessExample
from .base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "mask"


def create_process_description():
    p_data = Parameter(
        description="Any openEO process object that returns raster datasets "
        "or space-time raster dataset",
        schema={
            "type": "object",
            "subtype": "raster-cube"},
        optional=False)
    p_mask = Parameter(
        description="Any openEO process object that returns raster datasets "
        "or space-time raster dataset",
        schema={
            "type": "object",
            "subtype": "raster-cube"},
        optional=False)
    p_value = Parameter(
        description="The value used to replace non-zero and `true` values with",
        schema={
            "type": "object",
            "subtype": "string"},
        optional=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "data": {"from_node": "get_data_1"},
        "mask": {"from_node": "get_data_2"},
        "replacement": "null",
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "mask_1": node})
    examples = [
        ProcessExample(
            title="Simple example",
            description="Simple example",
            process_graph=graph)]

    pd = ProcessDescription(
        id=PROCESS_NAME,
        description="Applies a mask to a raster data cube "
        " replacing pixels in data that are not null in mask with the new value.",
        summary="Applies a mask to a raster data cube",
        parameters={
            "data": p_data,
            "mask": p_mask,
            "replacement": p_value},
        returns=rv,
        examples=[examples])

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(
        input_object: DataObject,
        mask_object: DataObject,
        mask_value: str,
        output_object: DataObject):
    """Create a Actinia command of the process chain that uses t.rast.mapcalc
    to mask raster values based on a mask dataset and a replacement value

    :param input_object: The input time series name
    :param mask_object: time series to use as mask
    :param mask_value: values in input are replaced with this value if mask is not null
    :param output_object: The output time series name
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    if mask_value == "null":
        mask_value = "null()"

    pc = []

    p = {"id": "t_rast_mask_%i" % rn,
          "module": "t.rast.mask",
          "inputs": [{"param": "input",
                      "value": input_object.grass_name()},
                     {"param": "mask",
                     "value": mask_object.grass_name()},
                     {"param": "basename",
                     "value": output_object.name},
                     {"param": "output",
                     "value": output_object.grass_name()},
                     {"param": "value",
                     "value": mask_value},
                     ],
          "flags": "i"}

    pc.append(p)

    p = {"id": "t_info_%i" % rn,
          "module": "t.info",
          "inputs": [{"param": "input", "value": output_object.grass_name()},
                     {"param": "type", "value": "strds"}],
          "flags": 'g'}

    pc.append(p)

    return pc


def get_process_list(node: Node) -> Tuple[list, list]:
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "data" not in node.arguments or \
            "mask" not in node.arguments:
        raise Exception(
            "Process %s requires parameter data, mask" %
            PROCESS_NAME)

    if "replacement" in node.arguments:
        mask_value = node.arguments["replacement"]
    else:
        mask_value = "null"

    # Get the input and mask data separately
    data_object = list(
        node.get_parent_by_name(
            parent_name="data").output_objects)[0]
    mask_object = list(
        node.get_parent_by_name(
            parent_name="mask").output_objects)[0]

    output_object = DataObject(
        name=create_output_name(data_object.name, node),
        datatype=GrassDataType.STRDS)
    output_objects.append(output_object)
    node.add_output(output_object=output_object)

    pc = create_process_chain_entry(
        data_object,
        mask_object,
        mask_value,
        output_object)
    process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
