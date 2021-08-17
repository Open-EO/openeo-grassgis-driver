# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import \
     ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import \
     Node, check_node_parents, DataObject, GrassDataType, \
     create_ouput_name
from openeo_grass_gis_driver.actinia_processing.base import \
     PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_schemas import \
     Parameter, ProcessDescription, ReturnValue, ProcessExample

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

# not in the official list
PROCESS_NAME = "percentile_time"


def create_process_description():
    p_data = Parameter(
        description="Any openEO process object that returns raster datasets "
        "or space-time raster dataset",
        schema={
            "type": "object",
            "subtype": "raster-cube"},
        optional=False)
    p_percentile = Parameter(description="The percentile to get from a "
                                         "space-time raster dataset",
                             schema={"type": "object", "subtype": "float"},
                             optional=False)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {"data": {"from_node": "get_strds_data"},
                 "percentile": "5"}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "percentile_time_1": node})
    examples = [
        ProcessExample(
            title="Simple example",
            description="Simple example",
            process_graph=graph)]

    pd = ProcessDescription(
        id=PROCESS_NAME,
        description="Reduce the time dimension of a space-time raster dataset "
        "by getting the percentile.",
        summary="Reduce the time dimension of a space-time raster dataset.",
        parameters={
            "data": p_data,
            "percentile": p_percentile},
        returns=rv,
        examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(
        input_object: DataObject,
        percentile,
        output_object: DataObject):
    """Create a Actinia process description that uses t.rast.series to reduce a time series.

    :param input_time_series: The input time series object
    :param percentile: The percentile to use for time reduction
    :param output_map: The object of the output raster map
    :return: A Actinia process chain description
    """
    rn = randint(0, 1000000)

    quantile = float(percentile) / 100.0

    pc = {"id": "t_rast_series_%i" % rn,
          "module": "t.rast.series",
          "inputs": [{"param": "input", "value": input_object.grass_name()},
                     {"param": "method", "value": "quantile"},
                     {"param": "quantile", "value": quantile},
                     {"param": "output", "value": output_object.grass_name()}],
          "flags": "t"}

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

    if "percentile" not in node.arguments:
        raise Exception("Parameter percentile is required.")

    for data_object in node.get_parent_by_name("data").output_objects:
        # multiple strds as input ?
        # multiple raster layers as output !
        output_object = DataObject(
            name=create_ouput_name(data_object.name, PROCESS_NAME),
            datatype=GrassDataType.STRDS)
        output_objects.append(output_object)
        node.add_output(output_object=output_object)

        pc = create_process_chain_entry(
            data_object, node.arguments["percentile"], output_object)
        process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
