# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import process_node_to_actinia_process_chain,\
    PROCESS_DICT, PROCESS_DESCRIPTION_DICT, ProcessNode
from openeo_grass_gis_driver.process_schemas import Parameter, ProcessDescription, ReturnValue
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "MAPCALC"


def create_process_description():

    p_a = Parameter(description="Any openEO process object that returns a single raster datasets identified as $A "
                                "in the r.mapcalc expression.",
                       schema={"type": "object", "format": "eodata"},
                      required=True)

    p_b = Parameter(description="Any openEO process object that returns a single raster datasets identified as $B "
                                "in the r.mapcalc expression.",
                       schema={"type": "object", "format": "eodata"},
                      required=True)

    p_c = Parameter(description="Any openEO process object that returns a single raster datasets identified as $C "
                                "in the r.mapcalc expression.",
                       schema={"type": "object", "format": "eodata"},
                      required=True)

    p_d = Parameter(description="Any openEO process object that returns a single raster datasets identified as $D "
                                "in the r.mapcalc expression.",
                       schema={"type": "object", "format": "eodata"},
                      required=True)

    p_e = Parameter(description="Any openEO process object that returns a single raster datasets identified as $E "
                                "in the r.mapcalc expression.",
                       schema={"type": "object", "format": "eodata"},
                      required=True)

    p_f = Parameter(description="Any openEO process object that returns a single raster datasets identified as $F "
                                "in the r.mapcalc expression.",
                       schema={"type": "object", "format": "eodata"},
                      required=True)

    p_result = Parameter(description="Any openEO process object that returns a single raster datasets identified as $RESULT "
                                "in the r.mapcalc expression.",
                       schema={"type": "object", "format": "eodata"},
                      required=True)

    p_expression = Parameter(description="The r.mapcalc expression",
                       schema={"type": "string", "examples": ["$RESULT = $A / $B", "$RESULT = ($A - $B)/($A + $B)"]},
                       required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    simple_example = {
        "mapcalc_1": {
            "process_id": PROCESS_NAME,
            "arguments": {
                "a": {"from_node": "get_a_data"},
                "b": {"from_node": "get_b_data"},
                "c": {"from_node": "get_c_data"},
                "d": {"from_node": "get_d_data"},
                "e": {"from_node": "get_e_data"},
                "f": {"from_node": "get_f_data"},
            }
        }
        }

    examples = dict(simple_example=simple_example)

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Use a r.macalc expression to compute a new raster "
                                        "dataset from up to 6 existing raster datasets.",
                            summary="Apply a r.mapcalc expression with up to 6 raster datasets.",
                            parameters={"a": p_a,
                                        "b": p_b,
                                        "c": p_c,
                                        "d": p_d,
                                        "e": p_e,
                                        "f": p_f,
                                        "result": p_result,
                                        "expression": p_expression
                                        },
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(expression: str):

    rn = randint(0, 1000000)

    pc = [
        {"id": "r_mapcalc_%i" % rn,
         "module": "t.rast.mapcalc",
         "inputs": [{"param": "expression",
                     "value": expression}]
        }]

    return pc


def get_process_list(node: ProcessNode):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param args: The process description arguments
    :return: (output_names, actinia_process_list)
    """

    input_names, process_list = process_node_to_actinia_process_chain(node)
    output_names = []

    if "result" not in node.arguments:
        raise Exception("The result name must be specified as parameter")

    if "expression" not in node.arguments:
        raise Exception("The expression must be specified as parameter")

    result = node.get_parent_by_name(parent_name="result").output_names[0]
    result = ActiniaInterface.layer_def_to_grass_map_name(result)

    expression = node.arguments["expression"]

    if "a" not in node.arguments:
        a = node.get_parent_by_name(parent_name="a").output_names[0]
        A = ActiniaInterface.layer_def_to_grass_map_name(a)
        expression = expression.replace("$A", A)
    if "b" not in node.arguments:
        b = node.get_parent_by_name(parent_name="b").output_names[0]
        B = ActiniaInterface.layer_def_to_grass_map_name(b)
        expression = expression.replace("$B", B)
    if "c" not in node.arguments:
        c = node.get_parent_by_name(parent_name="c").output_names[0]
        C = ActiniaInterface.layer_def_to_grass_map_name(c)
        expression = expression.replace("$C", C)
    if "d" not in node.arguments:
        d = node.get_parent_by_name(parent_name="d").output_names[0]
        D = ActiniaInterface.layer_def_to_grass_map_name(d)
        expression = expression.replace("$D", D)
    if "e" not in node.arguments:
        e = node.get_parent_by_name(parent_name="e").output_names[0]
        E = ActiniaInterface.layer_def_to_grass_map_name(e)
        expression = expression.replace("$E", E)
    if "f" not in node.arguments:
        f = node.get_parent_by_name(parent_name="f").output_names[0]
        F = ActiniaInterface.layer_def_to_grass_map_name(f)
        expression = expression.replace("$F", F)

    expression = expression.replace("$RESULT", result)

    output_names.append(result)
    node.add_output(output_name=result)

    pc = create_process_chain_entry(expression)
    process_list.extend(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
