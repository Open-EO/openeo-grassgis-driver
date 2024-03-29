# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import \
     ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import \
     PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
     check_node_parents, DataObject
from openeo_grass_gis_driver.models.process_schemas import \
     Parameter, ProcessDescription, ReturnValue, ProcessExample

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "save_result"


def create_process_description():
    p_data = Parameter(
        description="Any openEO process object that returns raster datasets "
        "or space-time raster dataset",
        schema={
            "type": "object",
            "subtype": "raster-cube"},
        optional=False)
    p_format = Parameter(
        description="The format of the export. Default is GeotTiff format.",
        schema={
            "type": "string",
            "default": "GTiff"},
        optional=True)
    p_options = Parameter(
        description="The file format parameters to be used to create the file(s).",
        schema={
            "type": "object",
            "subtype": "output-format-options",
            "default": {}},
        optional=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {"data": {"from_node": "get_b08_data"},
                 "format": "GTiff",
                 "options": {"COMPRESS": "DEFLATE"}}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "save_result_1": node})
    examples = [
        ProcessExample(
            title="Simple example",
            description="Simple example",
            process_graph=graph)]
    pd = ProcessDescription(
        id=PROCESS_NAME,
        description="This process exports an arbitrary number of raster map layers "
        "using the region specified upstream.",
        summary="Exports raster map layers using the region specified upstream.",
        parameters={
            "data": p_data,
            "format": p_format,
            "options": p_options},
        returns=rv,
        examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object: DataObject, options: dict):
    """Create a Actinia command of the process chain that computes the regional statistics based on a
    strds and a polygon.

    :param input_object: The name of the raster layer
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)
    pc = []

    output_format = "GTiff"
    if input_object.is_vector():
        output_format = "GML"

    # the actinia exporter currently does not support GDAL creation options
    # parameter options is ignored
    options_list = list()
    for key in options:
        optstr = ("%s=%s" % (key, options[key]))
        options_list.append(optstr)

    exporter = {"id": "save_result_%i" % rn,
                "module": "exporter",
                "outputs": [{"export": {"type": input_object.datatype.value,
                                        "format": output_format},
                             "param": "map",
                             "value": input_object.grass_name()}]}

    pc.append(exporter)

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result layer
    which is a single raster layer

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    options = {}
    if "options" in node.arguments:
        options = node.arguments["options"]

    # Pipe the inputs to the outputs
    for input_object in node.get_parent_by_name("data").output_objects:
        output_objects.append(input_object)
        node.add_output(output_object=input_object)

        pc = create_process_chain_entry(input_object=input_object,
                                        options=options)
        process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
