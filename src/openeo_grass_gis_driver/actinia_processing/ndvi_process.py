# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import \
     ProcessGraph, ProcessGraphNode
from openeo_grass_gis_driver.actinia_processing.base import \
     PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
     check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_schemas import \
     Parameter, ProcessDescription, ReturnValue, ProcessExample

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "ndvi"


def create_process_description():
    p_data = Parameter(
        description="A raster data cube with two bands that have the common names red and nir assigned.",
        schema={
            "type": "object",
            "subtype": "raster-cube"},
        optional=False)
    p_nir = Parameter(
        description="The name of the NIR band. Defaults to the band that has the common name `nir` assigned.",
        schema={
            "type": "string",
            "subtype": "band-name"},
        optional=True)
    p_red = Parameter(
        description="The name of the red band. Defaults to the band that has the common name `red` assigned.",
        schema={
            "type": "string",
            "subtype": "band-name"},
        optional=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "data": {"from_node": "get_data"},
        "nir": "S2_8",
        "red": "S2_4"
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "ndvi_1": node})
    examples = [
        ProcessExample(
            title="Simple example",
            description="Simple example",
            process_graph=graph)]

    pd = ProcessDescription(
        id=PROCESS_NAME,
        description="The data parameter expects a raster data cube with two bands "
        "that have the common names red and nir assigned. The process returns "
        "a raster data cube with two bands being replaced with a new band "
        "that holds the computed values. ",
        summary="Computes the Normalized Difference Vegetation Index (NDVI). "
        "The NDVI is computed as (nir - red) / (nir + red).",
        parameters={
            "data": p_data,
            "nir": p_nir,
            "red": p_red},
        returns=rv,
        examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_time_series: DataObject,
                               nir_band, red_band,
                               output_time_series: DataObject):
    """Create a Actinia process description that uses t.rast.ndvi to create the NDVI time series

    :param input_time_series: The input time series object with red and nir bands
    :param output_time_series: The object of the output time series
    :return: A list of Actinia process chain descriptions
    """
    rn = randint(0, 1000000)

    # TODO: adjust t.rast.ndvi to accept nir band and red band names
    #       pass nir_band and red_band to t.rast.ndvi

    pc = [
        {"id": "t_rast_ndvi_%i" % rn,
         "module": "t.rast.ndvi",
         "inputs": [{"param": "input",
                     "value": "%(input)s" % {"input": input_time_series.grass_name()}},
                    {"param": "basename",
                     "value": "ndvi"},
                    {"param": "output",
                     "value": output_time_series.grass_name()}]},
        {"id": "t_rast_color_%i" % rn,
         "module": "t.rast.colors",
         "inputs": [{"param": "input",
                     "value": output_time_series.grass_name()},
                    {"param": "color",
                     "value": "ndvi"}]}]

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    # Get the input data
    input_objects = node.get_parent_by_name(parent_name="data").output_objects

    input_strds = list(input_objects)[-1]

    nir_band = None
    red_band = None
    if "nir" in node.arguments and \
       node.arguments["nir"] is not None and \
       node.arguments["nir"] != "null":
        nir_band = node.arguments["nir"]
    if "red" in node.arguments and \
       node.arguments["red"] is not None and \
       node.arguments["red"] != "null":
        nir_band = node.arguments["red"]

    output_objects.extend(list(input_objects))

    output_object = DataObject(
        name=f"{input_strds.name}_{PROCESS_NAME}",
        datatype=GrassDataType.STRDS)
    output_objects.append(output_object)
    node.add_output(output_object=output_object)

    pc = create_process_chain_entry(
        input_strds, nir_band, red_band, output_object)
    process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
