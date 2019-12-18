# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import Node, check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"

PROCESS_NAME = "reduce"

OPERATOR_DICT = {
    'sum': '+',
    'subtract': '-',
    'product': '*',
    'divide': '/'
}

def create_process_description():
    p_data = Parameter(description="Raster data cube",
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


def create_process_chain_entry(input_object: DataObject, dimtype, formula,
                               operators, target_dimtype, output_object: DataObject):
    """Create a Actinia process description.

    :param input_object: The input time series object
    :param dimension: dimension to reduce
    :param output_object: The output time series or raster object
    :return: A Actinia process chain description
    """

    # dimension is the name of the dimension. The name is arbitrary.
    # Need to check the dimension name and get its type.
    # Supported dimension types are "temporal" and "bands".
    # Dimension type "spatial" should also be supported.
    # We can not check dimension names of the input object here
    # because the input object does not exist yet.
    # Use a new GRASS addon t.rast.reduce ?
    # There are no dimension names in GRASS, only dimension types
    # -> deadlock: dimension names are openeo specific
    #              we need the openeo object to get the dimension type
    #              from the dimension name
    #              BUT the openeo object does not exist yet
    # implement openeo / STAC like dimensions in GRASS ?
    
    rn = randint(0, 1000000)

    if dimtype == 'temporal':
        # t.rast.series

        # exactly one function: map openeo function to r.series method

        method = operators[0]
        if method == "mean":
            method = "average"
        elif method == "count":
            method = "count"
        elif method == "median":
            method = "median"
        elif method == "min":
            method = "minimum"
        elif method == "max":
            method = "maximum"
        elif method == "sd":
            method = "stddev"
        elif method == "sum":
            method = "sum"
        elif "variance" in formula:
            method = "variance"
        else :
            raise Exception('Unsupported method <%s> for temporal reduction.' % (method))

        # TODO: quantiles with openeo options probabilites (list of values between 0 and 1
        # q as number of intervals to calculate quantiles for
        
        pc = {"id": "t_rast_series_%i" % rn,
              "module": "t.rast.series",
              "inputs": [{"param": "input", "value": input_object.grass_name()},
                         {"param": "method", "value": method},
                         {"param": "output", "value": output_object.grass_name()}],
              "flags": "t"}

    elif dimtype == 'bands':
        # t.rast.mapcalc
        
        # TODO: new GRASS addon t.rast.bandcalc
        #       this addon needs the formula and 
        #       must translate "data[<index>]" to appropriate band numbers or names
        #       with <index> being a number, 0 for first band

        print (formula)
        pc = {"id": "t_rast_mapcalc_%i" % rn,
              "module": "t.rast.mapcalc",
         "inputs": [{"param": "expression",
                     "value": "%(result)s = %(formula)s" % {
                                                        "result": output_object.grass_name(),
                                                        "formula": formula}},
                    {"param": "inputs",
                     "value": "%(input)s" % {"input": input_object.grass_name()}},
                    {"param": "basename",
                     "value": "reduce"},
                    {"param": "output",
                     "value": output_object.grass_name()}]}



    return pc

def get_dimension_type(dimension_name):
    """Guess dimension type from dimension name.
    
    Problem: name and type of dimensions must be stored with the data
             and data do not exist yet, but we need the dimension type here
             in order to parse the openeo reducer
    """

    dimtype = None

    if dimension_name == 'temporal':
        dimtype = 'temporal'
    elif 'spectral' in dimension_name or 'band' in dimension_name:
        dimtype = 'bands'
    elif dimension_name in ('x', 'y', 'z', 'easting', 'northing', 'height'):
        dimtype = 'spatial'

    return dimtype

def construct_tree(obj):
    nodes = dict()
    root = None
    operators = []

    # TODO: process_id quantile

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
            operators.append(node['operator'])
        else:
            if config['process_id'] == 'array_element':
                node['type'] = 'inputdata'
                node['index'] = config['arguments']['index']
            else:
                node['operator'] = config['process_id']
                operators.append(node['operator'])
                node['children'] = []
        if config['result'] == True:
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
            results = []
            for node in tree['children']:
                results.append(serialize_tree(node))
            return operator + '(' + (', ').join(results) + ')'
            #return operator
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
    #raise Exception('The reducer process is not fully supported yet.')
    # get dimension type
    dimtype = get_dimension_type(node.arguments["dimension"])
    if dimtype is None:
        raise Exception('Unable to determine dimension type for dimension <%s>.' % (dimension))

    target_dimtype = None
    if "target_dimension" in node.arguments and node.arguments["target_dimension"] is not None:
        target_dimtype = get_dimension_type(node.arguments["target_dimension"])

    tree, operators = construct_tree(node.as_dict()['arguments']['reducer']['callback'])
    print (operators)
    formula = None
    output_datatype = GrassDataType.RASTER
    if dimtype == 'bands':
        formula = serialize_tree(tree)
        print (formula)
        output_datatype = GrassDataType.STRDS
    elif dimtype == 'temporal':
        if len(operators) != 1:
            raise Exception('Only one method is supported by reducer process on the temporal dimension.')

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    for input_object in node.get_parent_by_name("data").output_objects:

        output_object = DataObject(name=f"{input_object.name}_{PROCESS_NAME}", datatype=output_datatype)
        output_objects.append(output_object)
        node.add_output(output_object=output_object)

        pc = create_process_chain_entry(input_object,
                                        dimtype,
                                        formula,
                                        operators,
                                        target_dimtype,
                                        output_object)
        process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
