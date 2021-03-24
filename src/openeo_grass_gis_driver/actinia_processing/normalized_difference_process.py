# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph, ProcessGraphNode

from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
    check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Markus Metz, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "normalized_difference"


def create_process_description():
    p_band1 = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                        "that contains the first band for normalized difference computation.",
                        schema={"type": "object", "subtype": "raster-cube"},
                        optional=False)

    p_band2 = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                        "that contains the second band for normalized difference computation.",
                        schema={"type": "object", "subtype": "raster-cube"},
                        optional=False)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "band1": {"from_node": "get_band1_data"},
        "band2": {"from_node": "get_band2_data"},
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"nnormalized difference_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="The normalized difference is computed as *(band1 - band2) / (band1 + band2).",
                            summary="The normalized difference is computed as *(band1 - band2) / (band1 + band2).",
                            parameters={"band1": p_band1, "band2": p_band2},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(band1_time_series: DataObject, band2_time_series: DataObject,
                               output_time_series: DataObject):
    """Create a Actinia process description that uses t.rast.mapcalc to create the normalized difference time series

    :param band1_time_series: The first band time series object
    :param band2_time_series: The second band time series object
    :param output_time_series: The object of the output time series
    :return: A list of Actinia process chain descriptions
    """

    rn = randint(0, 1000000)

    pc = [
        {"id": "t_rast_mapcalc_%i" % rn,
         "module": "t.rast.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = float((%(band1)s - %(band2)s)/"
                              "(%(band1)s + %(band2)s))" % {"result": output_time_series.grass_name(),
                                                            "band1": band1_time_series.grass_name(),
                                                            "band2": band2_time_series.grass_name()}},
                    {"param": "inputs",
                     "value": "%(band1)s,%(band2)s" % {"band1": band1_time_series.grass_name(),
                                                       "band2": band2_time_series.grass_name()}},
                    {"param": "basename",
                     "value": "nd"},
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
    if "band1" not in node.arguments:
        raise Exception("Process %s requires parameter <band1>" % PROCESS_NAME)

    if "band2" not in node.arguments:
        raise Exception("Process %s requires parameter <band2>" % PROCESS_NAME)

    # Get the red and nir data separately
    band1_input_objects = node.get_parent_by_name(parent_name="band1").output_objects
    band2_input_objects = node.get_parent_by_name(parent_name="band2").output_objects

    if not band1_input_objects:
        raise Exception("Process %s requires an input strds for band 1" % PROCESS_NAME)

    if not band2_input_objects:
        raise Exception("Process %s requires an input strds for band 2" % PROCESS_NAME)

    band1_strds = list(band1_input_objects)[-1]
    band2_strds = list(band2_input_objects)[-1]

    output_objects.extend(list(band1_input_objects))
    output_objects.extend(list(band2_input_objects))

    output_object = DataObject(name=f"{band1_strds.name}_{PROCESS_NAME}", datatype=GrassDataType.STRDS)
    output_objects.append(output_object)
    node.add_output(output_object=output_object)

    pc = create_process_chain_entry(band1_strds, band2_strds, output_object)
    process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
