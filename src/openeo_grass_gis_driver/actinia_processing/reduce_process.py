# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import Node, check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"

# not in the official list
PROCESS_NAME = "reduce"
OPERATOR_DICT = {
    'sum': '+',
    'subtract': '-',
    'product': '*',
    'divide': '/'
}

def create_process_description():
    p_data = Parameter(description="Raster data qube",
                       schema={"type": "object", "format": "raster-cube"},
                       required=True)
    p_reducer = Parameter(description="The reducer",
                         schema={
                "anyOf": [
                    {
                        "title": "Unary behaviour",
                        "description": "Passes an array to the reducer.",
                        "type": "object",
                        "format": "callback",
                        "parameters": {
                            "data": {
                                "description": "An array with elements of any data type.",
                                "type": "array",
                                "items": {
                                    "description": "Any data type."
                                }
                            }
                        }
                    },
                    {
                        "title": "Binary behaviour",
                        "description": "Passes two values to the reducer.",
                        "type": "object",
                        "format": "callback",
                        "parameters": {
                            "x": {
                                "description": "The first value. Any data type could be passed."
                            },
                            "y": {
                                "description": "The second value. Any data type could be passed."
                            }
                        }
                    },
                    {
                        "title": "No operation behaviour",
                        "description": "Specifying `null` works only on dimensions with a single dimension value left. In this case the remaining value is treated like a reduction result and the dimension gets dropped.",
                        "type": "null"
                    }
                ],
                "default": "null"
            },
                         required=True)

    p_dimension = Parameter(description="The dimension",
                       schema={"type": "string"},
                       required=True)

    p_target_dimension = Parameter(description="The target dimension",
                       schema={"type": ["string", "null"],
                            "default": "null"})

    p_binary = Parameter(description="If binary",
                       schema={"type": "boolean",
                            "default": False})

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "raster-cube"})

    # Example
    arguments = {
                "data": {"from_node": "get_strds_data"},
                "dimension": "spatial",
                "target_dimension": "spatial",
                "reducer": "null"}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"reduce1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]
    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Reduce",
                            summary="Reduce",
                            parameters={"data": p_data, "reducer": p_reducer, "dimension": p_dimension, "target_dimension": p_target_dimension, "binary": p_binary},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object: DataObject, method, output_object: DataObject):
    """Create a Actinia process description that uses t.rast.series to reduce a time series.

    :param input_object: The input time series object
    :param method: The method for time reduction
    :param output_map: The name of the output raster object
    :return: A Actinia process chain description
    """
    rn = randint(0, 1000000)
    print (input_object)
    pc = {"id": "t_rast_series_%i" % rn,
          "module": "t.rast.series",
          "inputs": [{"param": "input", "value": input_object.grass_name()},
                     {"param": "method", "value": method},
                     {"param": "output", "value": output_object.grass_name()}],
          "flags": "t"}

    return pc


def construct_tree(obj):
    nodes = dict()
    root = None

    for name in obj:
        nodes[name] = {'type': 'node', 'children': []}

    for name, config in obj.items():
        node = nodes[name]
        args = config['arguments']['data']
        if isinstance(args, list):
            for arg in args:
                if isinstance(arg, dict):
                    ref_name = arg['from_node']
                    node['children'].append(nodes[ref_name])
                else:
                    node['children'].append({'type': 'literal', 'value': arg})
            node['operator'] = config['process_id']
        else:
            if config['process_id'] == 'array_element':
                node['type'] = 'inputdata'
                node['index'] = config['arguments']['index']
            else:
                node['operator'] = config['process_id']
                node['children'] = []
        if config['result'] == True:
            root = node
    return root

def serialize_tree(tree):
    if tree['type'] == 'node':
        operator = tree['operator']
        if operator in OPERATOR_DICT:
            operator = OPERATOR_DICT[tree['operator']]
            results = []
            for node in tree['children']:
                results.append(serialize_tree(node))
            return '(' + (' ' + operator + ' ').join(results) + ')'
        else:
            return operator
    if tree['type'] == 'literal':
        return str(tree['value'])
    if tree['type'] == 'inputdata':
        return 'data[' + str(tree['index']) + ']'

def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain
    and the name of the processing result layer
    which is a single raster layer

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """
    raise Exception('The reducer process is not fully supported yet.')
    tree = construct_tree(node.as_dict()['arguments']['reducer']['callback'])
    formula = serialize_tree(tree)
    print (formula)
    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "method" not in node.arguments:
        raise Exception("Parameter method is required.")

    for input_object in node.get_parent_by_name("data").output_objects:

        output_object = DataObject(name=f"{input_object.name}_{PROCESS_NAME}", datatype=GrassDataType.RASTER)
        output_objects.append(output_object)
        node.add_output(output_object=output_object)

        pc = create_process_chain_entry(input_object, node.arguments["method"], output_object)
        process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
