# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
    check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "filter_daterange"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                                   "or space-time raster dataset",
                       schema={"type": "object", "format": "eodata"},
                       required=True)

    p_from = Parameter(description="The start date of the filter in YYYY-MM-DD HH:mm:SS format",
                       schema={"type": "string", "examples": ["2018-01-01 00:30:00"]},
                       required=True)

    p_to = Parameter(description="The end date of the filter in YYYY-MM-DD HH:mm:SS format",
                     schema={"type": "string", "examples": ["2018-01-01 00:30:00"]},
                     required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    # Example
    arguments = {
                "data": {"from_node": "get_strds_data"},
                "from": "2001-01-01",
                "to": "2005-01-01",
            }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"filter_daterange_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Drops observations from a collection that have been "
                                        "captured between start and end date.",
                            summary="Drops observations from a collection",
                            parameters={"data": p_data, "from": p_from, "to": p_to},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create__process_chain_entry(input_object: DataObject, start_time: str, end_time: str, output_object: DataObject):
    """Create a Actinia command of the process chain that uses t.rast.extract to create a subset of a strds

    :param input_object: The input strds object
    :param start_time:
    :param end_time:
    :param output_object: The output strds object
    :return: A Actinia process chain description
    """

    start_time = start_time.replace('T', ' ')
    end_time = end_time.replace('T', ' ')

    # Get info about the time series to extract its resolution settings and bbox
    rn = randint(0, 1000000)

    pc = {"id": "t_rast_extract_%i" % rn,
          "module": "t.rast.extract",
          "inputs": [{"param": "input", "value": input_object.grass_name()},
                     {"param": "where", "value": "start_time >= '%(start)s' "
                                                 "AND end_time <= '%(end)s'" % {"start": start_time, "end": end_time}},
                     {"param": "output", "value": output_object.grass_name()},
                     {"param": "expression", "value": "1.0 * %s" % input_object.grass_name()},
                     {"param": "basename", "value": f"{input_object.name}_extract"},
                     {"param": "suffix", "value": "num"}]}

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result
    strds that was filtered by start and end date

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    for data_object in node.get_parent_by_name(parent_name="data").output_objects:

        # Skip if the datatype is not a strds and put the input into the output
        if data_object.is_strds() is False:
            output_objects.append(data_object)
            continue

        output_object = DataObject(name=f"{data_object.name}_{PROCESS_NAME}", datatype=GrassDataType.STRDS)
        output_objects.append(output_object)
        node.add_output(output_object=output_object)

        start_time = None
        end_time = None

        if "from" in node.arguments:
            start_time = node.arguments["from"]
        if "to" in node.arguments:
            end_time = node.arguments["to"]

        pc = create__process_chain_entry(input_object=data_object,
                                         start_time=start_time,
                                         end_time=end_time,
                                         output_object=output_object)
        process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
