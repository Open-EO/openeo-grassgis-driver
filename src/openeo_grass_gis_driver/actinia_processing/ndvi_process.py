# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph, ProcessGraphNode

from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
    check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "ndvi"


def create_process_description():
    p_red = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                                  "that contains the RED band for NDVI computation.",
                      schema={"type": "object", "format": "eodata"},
                      required=True)

    p_nir = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                                  "that contains the NIR band for NDVI computation.",
                      schema={"type": "object", "format": "eodata"},
                      required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    # Example
    arguments = {
        "red": {"from_node": "get_red_data"},
        "nir": {"from_node": "get_nir_data"},
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"ndvi_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Compute the NDVI based on the red and nir bands of the input datasets.",
                            summary="Compute the NDVI based on the red and nir bands of the input datasets.",
                            parameters={"red": p_red, "nir": p_nir},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(nir_time_series: DataObject, red_time_series: DataObject,
                               output_time_series: DataObject):
    """Create a Actinia process description that uses t.rast.mapcalc to create the NDVI time series

    :param nir_time_series: The NIR band time series object
    :param red_time_series: The RED band time series object
    :param output_time_series: The object of the output time series
    :return: A list of Actinia process chain descriptions
    """
    rn = randint(0, 1000000)

    pc = [
        {"id": "t_rast_mapcalc_%i" % rn,
         "module": "t.rast.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = float((%(nir)s - %(red)s)/"
                              "(%(nir)s + %(red)s))" % {"result":  output_time_series.grass_name(),
                                                        "nir": nir_time_series.grass_name(),
                                                        "red": red_time_series.grass_name()}},
                    {"param": "inputs",
                     "value": "%(nir)s,%(red)s" % {"nir": nir_time_series.grass_name(),
                                                   "red": red_time_series.grass_name()}},
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

    # First analyse the data entries
    if "red" not in node.arguments:
        raise Exception("Process %s requires parameter <red>" % PROCESS_NAME)

    if "nir" not in node.arguments:
        raise Exception("Process %s requires parameter <nir>" % PROCESS_NAME)

    # Get the red and nir data separately
    red_input_objects = node.get_parent_by_name(parent_name="red").output_objects
    nir_input_objects = node.get_parent_by_name(parent_name="nir").output_objects

    if not red_input_objects:
        raise Exception("Process %s requires an input strds for band <red>" % PROCESS_NAME)

    if not nir_input_objects:
        raise Exception("Process %s requires an input strds for band <nir>" % PROCESS_NAME)

    red_stds = list(red_input_objects)[-1]
    nir_strds = list(nir_input_objects)[-1]

    output_objects.extend(list(red_input_objects))
    output_objects.extend(list(nir_input_objects))

    output_object = DataObject(name=f"{red_stds.name}_{PROCESS_NAME}", datatype=GrassDataType.STRDS)
    output_objects.append(output_object)
    node.add_output(output_object=output_object)

    pc = create_process_chain_entry(nir_strds, red_stds, output_object)
    process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
