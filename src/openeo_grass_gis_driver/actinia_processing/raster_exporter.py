# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
    check_node_parents, DataObject
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "raster_exporter"


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

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {"data": {"from_node": "get_b08_data"},
                 "format": "GTiff"}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "raster_exporter_1": node})
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
            "format": p_format},
        returns=rv,
        examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(data_object: DataObject):
    """Create a Actinia command of the process chain that computes the regional statistics based on a
    strds and a polygon.

    :param data_object: The name of the raster layer
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)
    pc = []

    exporter = {
        "id": "exporter_%i" % rn,
        "module": "exporter",
        "outputs": [{"export": {"type": "raster", "format": "GTiff"},
                     "param": "map",
                     "value": data_object.grass_name()}]}

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

    # Pipe the inputs to the outputs
    for data_object in node.get_parent_by_name("data").output_objects:

        # Export raster maps
        if data_object.is_raster():
            output_objects.append(data_object)
            node.add_output(output_object=data_object)

            pc = create_process_chain_entry(data_object=data_object)
            process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
