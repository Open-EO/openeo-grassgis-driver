# -*- coding: utf-8 -*-
import json
from random import randint
from typing import Tuple

from openeo_grass_gis_driver.actinia_processing.base import \
     check_node_parents, DataObject, GrassDataType, \
     create_output_name
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

PROCESS_NAME = "filter_bands"


def create_process_description():
    p_data = Parameter(description="A data cube with bands.",
                       schema={"type": "object", "subtype": "raster-cube"},
                       optional=False)

    p_bands = Parameter(
        description="A list of band names. "
        "Either the unique band name or one of the common band names.",
        schema={
            "type": "array",
            "items": {
                "type": "string",
                "subtype": "band-name"}},
        optional=True)

    p_wavelengths = Parameter(
        description="A list of sub-lists with each sub-list consisting of two elements. "
        "The first element is the minimum wavelength and the second element "
        "is the maximum wavelength. Wavelengths are specified in micrometres (μm).", schema={
            "type": "array", "items": {
                "type": "array", "minItems": 2, "maxItems": 2, "items": {
                    "type": "number"}, "examples": [
                    [
                        [
                            0.45, 0.5], [
                                 0.6, 0.7]]]}}, optional=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "data": {"from_node": "get_data_1"},
        "bands": ["red", "nir"]
    }

    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "filter_bands_1": node})
    examples = [
        ProcessExample(
            title="Simple example",
            description="Simple example",
            process_graph=graph)]

    pd = ProcessDescription(
        id=PROCESS_NAME,
        description="Filters the bands in the data cube so that bands that "
        "don't match any of the criteria are dropped from the data cube.",
        summary="Filter the bands by name",
        parameters={
            "data": p_data,
            "bands": p_bands,
            "wavelengths": p_wavelengths},
        returns=rv,
        examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_time_series: DataObject,
                               bands, wavelengths,
                               output_time_series: DataObject):
    """Create a Actinia command of the process chain that uses g.region to create a valid computational region
    for the provide input strds

    :param north:
    :param south:
    :param east:
    :param west:
    :param crs:
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    # convert wavelengths to a string
    wvstring = None
    pc = None
    if wavelengths and bands:
        wvstring = (',').join(wavelengths)

        pc = {"id": "t_rast_filterbands_%i" % rn,
              "module": "t.rast.filterbands",
              "inputs": [{"param": "input",
                          "value": "%(input)s" % {"input": input_time_series.grass_name()}},
                         {"param": "bands",
                          "value": "%(bands)s" % {"bands": (',').join(bands)}},
                         {"param": "wavelengths",
                          "value": "%(wavelengths)s" % {"wavelengths": wvstring}},
                         {"param": "output",
                          "value": output_time_series.grass_name()}]}
    elif bands:
        pc = {"id": "t_rast_filterbands_%i" % rn,
              "module": "t.rast.filterbands",
              "inputs": [{"param": "input",
                          "value": "%(input)s" % {"input": input_time_series.grass_name()}},
                         {"param": "bands",
                          "value": "%(bands)s" % {"bands": (',').join(bands)}},
                         {"param": "output",
                          "value": output_time_series.grass_name()}]}
    elif wavelengths:
        wvstring = (',').join(wavelengths)
        pc = {"id": "t_rast_filterbands_%i" % rn,
              "module": "t.rast.filterbands",
              "inputs": [{"param": "input",
                          "value": "%(input)s" % {"input": input_time_series.grass_name()}},
                         {"param": "bands",
                          "value": "%(bands)s" % {"bands": (',').join(bands)}},
                         {"param": "output",
                          "value": output_time_series.grass_name()}]}

    return pc


def get_process_list(node: Node) -> Tuple[list, list]:
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    # at least one of bands, common_names, wavelengths must be given
    if "data" not in node.arguments or \
            ("bands" not in node.arguments and
             "wavelengths" not in node.arguments):
        raise Exception(
            "Process %s requires parameter data and at least one of "
            "bands, wavelengths" %
            PROCESS_NAME)

    bands = None
    if "bands" in node.arguments:
        bands = node.arguments["bands"]
    wavelengths = None
    if "wavelengths" in node.arguments:
        wavelengths = node.arguments["wavelengths"]

    data_object = list(node.get_parent_by_name(
        parent_name="data").output_objects)[-1]

    output_object = DataObject(
        name=create_output_name(data_object.name, PROCESS_NAME),
        datatype=GrassDataType.STRDS)
    output_objects.append(output_object)
    node.add_output(output_object=output_object)

    pc = create_process_chain_entry(data_object, bands, wavelengths,
                                    output_object)
    process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
