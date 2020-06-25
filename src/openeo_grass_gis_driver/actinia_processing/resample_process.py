# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import Node, check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "resample_cube_spatial"


def create_process_description():
    # see https://github.com/Open-EO/openeo-processes/blob/master/resample_cube_spatial.json

    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "format": "raster-cube"},
                       required=True)
    p_target = Parameter(description="Any openEO process object that returns a raster dataset",
                         schema={"type": "object", "format": "raster-cube"},
                         required=True)
    p_method = Parameter(description="The resampling method to use",
                         schema={"type": "string"},
                         required=True)

    p_method.enum = ["near",
                     "bilinear",
                     "cubic",
                     "lanczos",
                     "average",
                     "mode",
                     "max",
                     "min",
                     "med",
                     "q1",
                     "q3"
                     ]

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "raster-cube"})

    # Example
    arguments = {"data": {"from_node": "get_strds_data_1"},
                 "target": {"from_node": "get_data_2"},
                 "method": "average"}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"resample_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Resample the spatial dimensions (x,y) from a source data cube "
                                        "to a target data cube and return the results as a new data cube.",
                            summary="Spatially resample a space-time raster dataset.",
                            parameters={"data": p_data, "target": p_target, "method": p_method},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object: DataObject, method, output_object: DataObject):
    """Create a Actinia process description.

    :param input_object: The input time series name
    :param method: The method for time reduction
    :param output_map: The name of the output raster map
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    # TODO: a new GRASS addon that
    # 1. fetches a list of raster maps in a strds
    # 2. resamples each raster map with the selected method
    
    # translate openeo method to GRASS method
    if method == "near":
        method = "nearest"
    if method == "cubic":
        method = "bicubic"
    if method == "max":
        method = "maximum"
    if method == "min":
        method = "minimum"
    if method == "med":
        method = "median"
    if method == "q1":
        method = "quart1"
    if method == "q3":
        method = "quart3"

    pc = [
        {"id": "t_rast_resample_%i" % rn,
         "module": "t.rast.resample",
         "inputs": [{"param": "input", "value": input_object.grass_name()},
                    {"param": "method", "value": method},
                    {"param": "output", "value": output_object.grass_name()}],
         }
    ]

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

    if "method" not in node.arguments:
        raise Exception("Parameter method is required.")

    for input_object in node.get_parent_by_name("data").output_objects:
        # multiple strds as input ?
        # multiple raster layers as output !
        output_object = DataObject(name=f"{input_object.name}_{PROCESS_NAME}", datatype=GrassDataType.STRDS)
        output_objects.append(output_object)
        node.add_output(output_object=output_object)

        pc = create_process_chain_entry(input_object, node.arguments["method"], output_object)
        process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
