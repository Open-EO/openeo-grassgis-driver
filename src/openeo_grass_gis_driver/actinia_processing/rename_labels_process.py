# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
    check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Markus Metz, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "rename_labels"


def create_process_description():
    p_data = Parameter(description="The data cube.",
                       schema={"type": "object", "subtype": "raster-cube"},
                       required=True)

    p_dim = Parameter(description="The name of the dimension to rename the labels for.",
                      schema={"type": "string"},
                      required=True)

    p_tgt = Parameter(description="The new names for the labels. The dimension labels in the data cube are expected to be enumerated, if the parameter `target` is not specified. If a target dimension label already exists in the data cube, a `LabelExists` error is thrown.",
                      schema={"type": "array",
                                "items": {
                                  "anyOf": [
                                    {
                                      "type": "number"
                                    },
                                    {
                                      "type": "string"
                                    }
                                  ]
                                }
                              },
                      required=True)

    p_src = Parameter(description="The names of the labels as they are currently in the data cube. The array defines an unsorted and potentially incomplete list of labels that should be renamed to the names available in the corresponding array elements in the parameter `target`. If one of the source dimension labels doesn't exist, a `LabelNotAvailable` error is thrown. By default, the array is empty so that the dimension labels in the data cube are expected to be enumerated.",
                      schema={"type": "array",
                                "items": {
                                  "anyOf": [
                                    {
                                      "type": "number"
                                    },
                                    {
                                      "type": "string"
                                    }
                                  ]
                                }
                              },
                      required=False)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
                "data": {"from_node": "get_strds_data"},
                "dimension": "bands",
                "target": "red"
            }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"rename_labels_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Limits the data cube to the specified interval of dates and/or times.",
                            summary="Temporal filter for a date and/or time interval",
                            parameters={"data": p_data, "dimension": p_dim, "target": p_tgt, "source": p_src},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create__process_chain_entry(input_object: DataObject, target, source, output_object: DataObject):
    """Create a Actinia command of the process chain that uses
       t.rast.renamebands to rename band names.

    :param input_object: The input strds object
    :param dimension:
    :param target:
    :param source:
    :param output_object: The output strds object
    :return: A Actinia process chain description
    """

    start_time = start_time.replace('T', ' ')
    end_time = end_time.replace('T', ' ')

    # Get info about the time series to extract its resolution settings and bbox
    rn = randint(0, 1000000)

    # source can be null
    if source:
        pc = {"id": "t_rast_renamebands_%i" % rn,
          "module": "t.rast.renamebands",
          "inputs": [{"param": "input", "value": input_object.grass_name()},
                     {"param": "target", "value": (',').join(target)},
                     {"param": "source", "value": (',').join(source)},
                     {"param": "output", "value": output_object.grass_name()}]}
    else:
        pc = {"id": "t_rast_renamebands_%i" % rn,
          "module": "t.rast.renamebands",
          "inputs": [{"param": "input", "value": input_object.grass_name()},
                     {"param": "target", "value": (',').join(target)},
                     {"param": "output", "value": output_object.grass_name()}]}

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result
    strds that was filtered by start and end date

    :param node: The process node
    :return: (output_names, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    for data_object in node.get_parent_by_name(parent_name="data").output_objects:

        # Skip if the datatype is not a strds and put the input into the output
        if data_object.is_strds() is False:
            output_objects.append(data_object)
            continue

        if "dimension" not in node.arguments or \
                node.arguments["dimension"] != "bands":
            raise Exception("Process %s requires dimension to be set to bands" % PROCESS_NAME)

        output_object = DataObject(name=f"{data_object.name}_{PROCESS_NAME}", datatype=GrassDataType.STRDS)
        output_objects.append(output_object)
        node.add_output(output_object=output_object)

        if not isinstance(node.arguments["target"], list):
            raise Exception("Process %s requires target to be a list" % PROCESS_NAME)
        target = node.arguments["target"]
        source = None
        if "source" in node.arguments:
            if not isinstance(node.arguments["source"], list):
                raise Exception("Process %s requires source to be a list" % PROCESS_NAME)
            source = node.arguments["source"]
            if len(source) != len(target):
                raise Exception("Process %s requires source and target to have the same number of items" % PROCESS_NAME)
        else:
            if len(target) != 1:
                raise Exception("Process %s requires one item in target if source is not given" % PROCESS_NAME)

        pc = create__process_chain_entry(input_object=data_object,
                                         target=target,
                                         source=source,
                                         output_object=output_object)
        process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
