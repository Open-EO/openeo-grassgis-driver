# -*- coding: utf-8 -*-
import json
from random import randint
from typing import Tuple

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from .base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

# not in the official list
PROCESS_NAME = "mask_invalid_values"


def create_process_description():
    p_data = Parameter(
        description="Any openEO process object that returns raster datasets "
        "or space-time raster dataset",
        schema={
            "type": "object",
            "subtype": "raster-cube"},
        optional=False)
    p_min = Parameter(description="Minimum allowed value",
                      schema={"type": "object", "subtype": "float"},
                      optional=False)
    p_max = Parameter(description="Maximum allowed value",
                      schema={"type": "object", "subtype": "float"},
                      optional=False)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    examples = {
        "mask_invalid_values_1": {
            "process_id": PROCESS_NAME,
            "arguments": {
                "data": {"from_node": "get_data_1"},
                "min": 1,
                "max": 150,
            }
        }
    }

    # Example
    arguments = {
        "data": {"from_node": "get_data_1"},
        "mask": {"from_node": "get_data_2"},
        "value": "null",
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
        description="Drops observations from raster data or raster time series data "
        " that are outside of the specified interval.",
        summary="Filter raster based data on the specified interval",
        parameters={
            "data": p_data,
            "min": p_min,
            "max": p_max},
        returns=rv,
        examples=[examples])

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(
        input_object: DataObject,
        vmin: float,
        vmax: float,
        output_object: DataObject):
    """Create a Actinia command of the process chain that uses t.rast.mapcalc
    to filter raster values by the specified interval

    :param input_object: The input time series object
    :param min: smallest allowed value
    :param max: largest allowed value
    :param output_object: The output time series object
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    pc = {"id": "t_rast_mapcalc_%i" % rn,
          "module": "t.rast.mapcalc",
          "inputs": [{"param": "expression",
                     "value": "%(result)s = if(%(raw)s < %(min)s || "
                              "%(raw)s > %(max)s), null(), %(raw)s)" % {"result": output_object.grass_name(),
                                                                        "raw": input_object.grass_name(),
                                                                        "min": str(vmin),
                                                                        "max": str(vmax)}},
                     {"param": "basename",
                     "value": "masked_invalid"},
                     {"param": "output",
                     "value": output_object.grass_name()},
                     ]}

    return pc


def get_process_list(node: Node) -> Tuple[list, list]:
    """Analyse the process node and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "data" not in node.arguments or \
            "min" not in node.arguments or \
            "max" not in node.arguments:
        raise Exception(
            "Process %s requires parameter data, min, max" %
            PROCESS_NAME)

    vmin = node.arguments["min"]
    vmax = node.arguments["max"]

    for data_object in input_objects:

        output_object = DataObject(
            name=f"{data_object.name}_{PROCESS_NAME}",
            datatype=GrassDataType.STRDS)
        output_objects.append(output_object)
        node.add_output(output_object=output_object)

        pc = create_process_chain_entry(data_object, vmin, vmax, output_object)
        process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
