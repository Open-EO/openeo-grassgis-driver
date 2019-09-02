# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import Node, check_node_parents
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "percentile_time"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)
    p_percentile = Parameter(description="The percentile to get from a "
                                         "space-time raster dataset",
                             schema={"type": "object", "format": "float"},
                             required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    # Example
    arguments = {"data": {"from_node": "get_strds_data"},
                 "percentile": "5"}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"percentile_time_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph, arguments=arguments)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Reduce the time dimension of a space-time raster dataset "
                                        "by getting the percentile.",
                            summary="Reduce the time dimension of a space-time raster dataset.",
                            parameters={"imagery": p_data, "percentile": p_percentile},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_name, percentile, output_name):
    """Create a Actinia process description that uses t.rast.series to reduce a time series.

    :param input_time_series: The input time series name
    :param percentile: The percentile to use for time reduction
    :param output_map: The name of the output raster map
    :return: A Actinia process chain description
    """
    input_name = ActiniaInterface.layer_def_to_grass_map_name(input_name)

    rn = randint(0, 1000000)

    quantile = float(percentile) / 100.0

    pc = {"id": "t_rast_series_%i" % rn,
          "module": "t.rast.series",
          "inputs": [{"param": "input", "value": input_name},
                     {"param": "method", "value": "quantile"},
                     {"param": "quantile", "value": quantile},
                     {"param": "output", "value": output_name}],
          "flags": "t"}

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain
    and the name of the processing result layer
    which is a single raster layer

    :param node: The process node
    :return: (output_names, actinia_process_list)
    """

    input_names, process_list = check_node_parents(node=node)
    output_names = []

    if "percentile" not in node.arguments:
        raise Exception("Parameter percentile is required.")

    for input_name in node.get_parent_by_name("data").output_names:
        # multiple strds as input ?
        # multiple raster layers as output !
        location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
        output_name = "%s_%s" % (layer_name, PROCESS_NAME)
        output_names.append(output_name)
        node.add_output(output_name=output_name)

        pc = create_process_chain_entry(input_name, node.arguments["percentile"], output_name)
        process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
