# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
    check_node_parents, DataObject, GrassDataType
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "temporal_algebra"


def create_process_description():
    p_a = Parameter(description="Any openEO process object that returns a single space-time raster "
                                "datasets identified as $a in the t.rast.algebra expression.",
                    schema={"type": "object", "subtype": "raster-cube"},
                    required=False)

    p_b = Parameter(description="Any openEO process object that returns a single space-time raster "
                                "datasets identified as $b in the t.rast.algebra expression.",
                    schema={"type": "object", "subtype": "raster-cube"},
                    required=False)

    p_c = Parameter(description="Any openEO process object that returns a single space-time raster "
                                "datasets identified as $c in the t.rast.algebra expression.",
                    schema={"type": "object", "subtype": "raster-cube"},
                    required=False)

    p_d = Parameter(description="Any openEO process object that returns a single space-time raster "
                                "datasets identified as $d in the t.rast.algebra expression.",
                    schema={"type": "object", "subtype": "raster-cube"},
                    required=False)

    p_e = Parameter(description="Any openEO process object that returns a single space-time raster "
                                "datasets identified as $e in the t.rast.algebra expression.",
                    schema={"type": "object", "subtype": "raster-cube"},
                    required=False)

    p_f = Parameter(description="Any openEO process object that returns a single space-time raster "
                                "datasets identified as $f in the t.rast.algebra expression.",
                    schema={"type": "object", "subtype": "raster-cube"},
                    required=False)

    p_result = Parameter(description="Any openEO process object that returns a single space-time raster datasets "
                                     "identified as RESULT in the t.rast.algebra expression.",
                         schema={"type": "object", "subtype": "raster-cube"},
                         required=True)

    p_expression = Parameter(description="The t.rast.algebra expression",
                             schema={"type": "string",
                                     "examples": ["$result = ($a + $b / ($a - $b))"]},
                             required=True)

    bn = Parameter(description="Basename of the new generated raster datasets in the resulting "
                               "space-time raster datasets",
                   schema={"type": "string", "examples": ["ndvi_base"]}, required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {
        "a": {"from_node": "get_a_data"},
        "b": {"from_node": "get_b_data"},
        "result": "ndvi",
        "basename": "ndvi_base",
        "expression": "$result = ($a + $b / ($a - $b))"
    }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"t_rast_algebra_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Use a t.rast.algebra expression to compute a new space-time raster "
                                        "dataset from up to 6 existing space-time raster datasets.",
                            summary="Apply a t.rast.algebra expression with up to 6 space-time raster datasets.",
                            parameters={"a": p_a,
                                        "b": p_b,
                                        "c": p_c,
                                        "d": p_d,
                                        "e": p_e,
                                        "f": p_f,
                                        "result": p_result,
                                        "expression": p_expression,
                                        "basename": bn
                                        },
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(expression: str, basename: str):
    rn = randint(0, 1000000)

    pc = [
        {"id": "t_rast_algebra_%i" % rn,
         "module": "t.rast.algebra",
         "inputs": [{"param": "expression",
                     "value": expression},
                    {"param": "basename",
                     "value": basename}
                    ]
         }]

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    if "result" not in node.arguments:
        raise Exception("The result name must be specified as parameter")
    if "expression" not in node.arguments:
        raise Exception("The expression must be specified as parameter")
    if "basename" not in node.arguments:
        raise Exception("The basename must be specified as parameter")

    result = DataObject(name=node.arguments["result"], datatype=GrassDataType.STRDS)

    expression = node.arguments["expression"]
    basename = node.arguments["basename"]

    if "a" in node.arguments:
        a = list(node.get_parent_by_name(parent_name="a").output_objects)[-1]
        expression = expression.replace("$a", a.grass_name())
    if "b" in node.arguments:
        b = list(node.get_parent_by_name(parent_name="b").output_objects)[-1]
        expression = expression.replace("$b", b.grass_name())
    if "c" in node.arguments:
        c = list(node.get_parent_by_name(parent_name="c").output_objects)[-1]
        expression = expression.replace("$c", c.grass_name())
    if "d" in node.arguments:
        d = list(node.get_parent_by_name(parent_name="d").output_objects)[-1]
        expression = expression.replace("$d", d.grass_name())
    if "e" in node.arguments:
        e = list(node.get_parent_by_name(parent_name="e").output_objects)[-1]
        expression = expression.replace("$e", e.grass_name())
    if "f" in node.arguments:
        f = list(node.get_parent_by_name(parent_name="f").output_objects)[-1]
        expression = expression.replace("$f", f.grass_name())

    expression = expression.replace("$result", result.grass_name())

    output_objects.append(result)
    node.add_output(output_object=result)

    pc = create_process_chain_entry(expression=expression, basename=basename)
    process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
