# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import Node, check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample

__license__ = "Apache License, Version 2.0"

PROCESS_NAME = "apply"

# translate openeo operators to r.mapcalc operators
OPERATOR_DICT = {
    'sum': '+',
    'subtract': '-',
    'multiply': '*',
    'product': '*',
    'divide': '/'
}

# translate openeo functions to r.mapcalc functions
FN_DICT = {
    'abs': 'abs',
    'ln': 'log',
    'power': 'pow'
}


def create_process_description():
    p_data = Parameter(description="Raster data cube",
                       schema={"type": "object", "subtype": "raster-cube"},
                       optional=False)
    p_uprocess = Parameter(description="Applies a unary process to each pixel value in the data cube. "
                                       "A unary process takes a single value and returns a single value.",
                           schema={"type": "object",
                                   "subtype": "process-graph",
                                   "parameters": [{
                                       "name": "x",
                                       "description": "The value to process.",
                                       "schema": {
                                          "description": "Any data type."
                                         }
                                      }]
                                   },
                           optional=False)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "data": {"from_node": "get_strds_data"},
        "process": "null"}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"apply1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]
    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Applies a **unary** process which takes a single value "
                                        "such as `abs` or `sqrt` to each pixel value and returns "
                                        "a single new value for each pixel",
                            summary="Applies a unary process to each pixel",
                            parameters={"data": p_data,
                                        "process": p_uprocess},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object: DataObject, formula,
                               operators, output_object: DataObject):
    """Create a Actinia process description.

    :param input_object: The input time series object
    :param output_object: The output time series or raster object
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    # t.rast.mapcalc

    pc = {"id": "t_rast_mapcalc_%i" % rn,
          "module": "t.rast.mapcalc",
          "inputs": [{"param": "expression",
                      "value": "%(formula)s" % {"formula": formula}},
                     {"param": "input",
                      "value": "%(input)s" % {"input": input_object.grass_name()}},
                     {"param": "output",
                      "value": output_object.grass_name()}]}

    return pc


def construct_tree(obj):
    nodes = dict()
    root = None
    operators = []

    # TODO: for process_id quantile, remember probabilities and q

    for name in obj:
        nodes[name] = {'type': 'node', 'children': []}

    for name, config in obj.items():
        node = nodes[name]
        if "data" in config['arguments']:
            args = config['arguments']['data']
        else:
            args = list()
            if "x" in config['arguments']:
                args.append(config['arguments']['x'])
            if "y" in config['arguments']:
                args.append(config['arguments']['y'])
        if isinstance(args, list):
            for arg in args:
                if isinstance(arg, dict):
                    ref_name = arg['from_node']
                    node['children'].append(nodes[ref_name])
                else:
                    node['children'].append({'type': 'literal', 'value': arg})
            node['operator'] = config['process_id']
            operators.append(node['operator'])
        else:
            if config['process_id'] == 'array_element':
                node['type'] = 'inputdata'
                node['index'] = config['arguments']['index']
            else:
                node['operator'] = config['process_id']
                operators.append(node['operator'])
                node['children'] = []
        if "result" in config and config['result'] is True:
            root = node
    return root, operators


# use only for dimension "bands"
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
            if operator in FN_DICT:
                operator = FN_DICT[tree['operator']]
            results = []
            for node in tree['children']:
                results.append(serialize_tree(node))
            # TODO: normalized_difference(x, y) -> (x - y) / (x + y)
            return operator + '(' + (', ').join(results) + ')'
            # return operator
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

    tree, operators = construct_tree(node.as_dict()['arguments']['process']['process_graph'])
    # print (operators)
    formula = None
    output_datatype = GrassDataType.RASTER
    formula = serialize_tree(tree)
    # print (formula)
    output_datatype = GrassDataType.STRDS

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    for input_object in node.get_parent_by_name("data").output_objects:

        output_object = DataObject(name=f"{input_object.name}_{PROCESS_NAME}", datatype=output_datatype)
        output_objects.append(output_object)
        node.add_output(output_object=output_object)

        pc = create_process_chain_entry(input_object,
                                        formula,
                                        operators,
                                        output_object)
        process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
