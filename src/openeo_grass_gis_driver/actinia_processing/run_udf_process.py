# -*- coding: utf-8 -*-
import json
from openeo_grass_gis_driver.models.process_graph_schemas import \
     ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import \
     Node, check_node_parents, DataObject, GrassDataType, \
     create_output_name
from openeo_grass_gis_driver.actinia_processing.base import \
     PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.models.process_schemas import \
     Parameter, ProcessDescription, ReturnValue, ProcessExample

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "run_udf"


def create_process_description():
    p_data = Parameter(description="The data to be passed to the UDF as array or raster data cube.",
                       schema=[
                           {
                               "title": "Raster data cube",
                               "type": "object",
                               "subtype": "raster-cube"
                           },
                           {
                               "title": "Array",
                               "type": "array",
                               "minItems": 1,
                               "items": {
                                    "description": "Any data type."
                                  }
                           },
                           {
                               "title": "Single Value",
                               "description": "A single value of any data type."
                           }
                       ],
                       optional=False)
    p_udf = Parameter(description="Either source code, an absolute URL or a path to an UDF script.",
                      schema=[{"description": "URI to an UDF",
                               "type": "string",
                               "format": "uri",
                               "subtype": "uri"},
                              {"description": "Path to an UDF uploaded to the server.",
                               "type": "string",
                               "subtype": "file-path"},
                              {"description": "Source code as string",
                               "type": "string",
                               "subtype": "udf-code"}],
                      optional=False)

    p_runtime = Parameter(
        description="An UDF runtime identifier available at the back-end.",
        schema={
            "type": "string",
            "subtype": "udf-runtime"},
        optional=False)

    p_version = Parameter(description="An UDF runtime version. If set to `null`, "
                          "the default runtime version specified for each runtime is used.",
                          schema=[{"type": "string",
                                   "subtype": "udf-runtime-version"},
                                  {"title": "Default runtime version",
                                   "type": "null"}],
                          optional=True)

    p_context = Parameter(
        description="Additional data such as configuration options "
        "that should be passed to the UDF.", schema={
            "type": "object"}, optional=True)

    rv = ReturnValue(
        description="The data processed by the UDF. Returns a raster data cube "
        "if a raster data cube was passed for `data`. If an array was "
        "passed for `data`, the returned value is defined by the context "
        "and is exactly what the UDF returned.", schema=[
            {
                "title": "Raster data cube", "type": "object", "subtype": "raster-cube"}, {
                 "title": "Any", "description": "Any data type."}])

    # Example
    arguments = {
        "data": {"from_node": "get_strds_data"},
        "udf": "some source code"}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(
        title="title",
        description="description",
        process_graph={
            "run_udf1": node})
    examples = [
        ProcessExample(
            title="Simple example",
            description="Simple example",
            process_graph=graph)]
    pd = ProcessDescription(
        id=PROCESS_NAME,
        description="Runs an UDF in one of the supported runtime environments.",
        summary="Run an UDF",
        parameters={
            "data": p_data,
            "udf": p_udf,
            "runtime": p_runtime,
            "version": p_version,
            "context": p_context},
        returns=rv,
        examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object, python_file_url,
                               udf_runtime, udf_version, output_object):
    """Create a Actinia command of the process chain that uses t.rast.udf

    :param strds_name: The name of the strds
    :param python_file_url: The URL to the python file that defines the UDF
    :param output_name: The name of the output raster layer
    :return: A Actinia process chain description
    """

    # rn = randint(0, 1000000)

    pc = {"id": "t_rast_udf",
          "module": "t.rast.udf",
          "inputs": [{"import_descr": {"source": python_file_url,
                                       "type": "file"},
                      "param": "pyfile",
                      "value": "$file::my_py_func"},
                     {"param": "input",
                      "value": input_object.grass_name()},
                     {"param": "output",
                      "value": output_object.grass_name()}]}

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain
    and the name of the processing result layer which is a single raster layer

    :param args: The process description
    :return: (output_names, actinia_process_list)
    """

    # Get the input description and the process chain to attach this process
    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    input_objects = node.get_parent_by_name(parent_name="data").output_objects

    python_file_url = node.arguments["udf"]
    udf_runtime = None
    if "runtime" in node.arguments:
        udf_runtime = node.arguments["runtime"]
    udf_version = None
    if "version" in node.arguments:
        udf_version = node.arguments["version"]

    for input_object in input_objects:

        output_object = DataObject(
            name=create_output_name(input_object.name, node),
            datatype=GrassDataType.STRDS)
        output_objects.append(output_object)

        pc = create_process_chain_entry(input_object,
                                        python_file_url,
                                        udf_runtime, udf_version,
                                        output_object)
        process_list.append(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
