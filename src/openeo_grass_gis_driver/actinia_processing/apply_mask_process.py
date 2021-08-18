# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import \
    Node, check_node_parents, DataObject, GrassDataType, \
    create_output_name
from openeo_grass_gis_driver.actinia_processing.base import \
    PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_graph_schemas import \
    ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import \
    Parameter, ProcessDescription, ReturnValue, ProcessExample

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

# not in the official list
PROCESS_NAME = "apply_mask"


def create_process_description():
    p_data = Parameter(
        description="Any openEO process object that returns raster datasets "
        "or a space-time raster dataset",
        schema={
            "type": "object",
            "subtype": "raster-cube"},
        optional=False)

    p_mask = Parameter(
        description="Any openEO process object that returns raster datasets "
        "or a space-time raster dataset",
        schema={
            "type": "object",
            "subtype": "raster-cube"},
        optional=False)

    rv = ReturnValue(description="Masked EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "data": {"from_node": "get_strds_data"},
        "mask": {"from_node": "get_mask_data"},
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "apply_mask_1": node})
    examples = [
        ProcessExample(
            title="Simple example",
            description="Simple example",
            process_graph=graph)]

    pd = ProcessDescription(
        id=PROCESS_NAME,
        description="Applies a mask to an EO dataset. "
        "Each pixel that is 0 or nodata in the mask is set to nodata. "
        "See also multilayer_mask.",
        summary="Apply a mask to an EO dataset.",
        parameters={
            "data": p_data,
            "mask": p_mask},
        returns=rv,
        examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(
        input: DataObject,
        mask: DataObject,
        output: DataObject):
    """Create a Actinia process description that uses r.mapcalc
       to apply a mask.

       NOTE: according to multilayer_mask, 0 means not masked, 1 means masked
             this is the other way around compared to GRASS

    :param input: The input map name
    :param mask: The mask map name
    :param output: The name of the output map
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    pc = {"id": "r_mapcalc_%i" % rn,
          "module": "r.mapcalc",
          "inputs": [{"param": "expression",
                      "value": "%(result)s = if(isnull(%(mask)s) || %(mask)s == 0, "
                      "null(), %(raw)s)" % {"result": output.grass_name(),
                                            "raw": input.grass_name(),
                                            "mask": mask.grass_name()}}]}

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

    if "mask" not in node.arguments:
        raise Exception("Parameter mask is required.")

    nmasks = len(node.get_parent_by_name("mask").output_objects)
    ninputs = len(node.get_parent_by_name("data").output_objects)

    if nmasks > 1 and nmasks != ninputs:
        raise Exception(
            "Either a single mask or a separate mask for each layer is required.")

    mask_object = None
    if nmasks == 1:
        mask_object = node.get_parent_by_name("mask").output_objects[0]

    for i in range(len(node.get_parent_by_name("data").output_objects)):
        input_object = node.get_parent_by_name("data").output_objects[i]
        if nmasks > 1:
            mask_object = node.get_parent_by_name("mask").output_objects[i]

        output_object = DataObject(
            name=create_output_name(input_object.name, PROCESS_NAME),
            datatype=GrassDataType.RASTER)
        output_objects.append(output_object)
        node.add_output(output_object=output_object)

        pc = create_process_chain_entry(
            input_object, mask_object, output_object)
        process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
