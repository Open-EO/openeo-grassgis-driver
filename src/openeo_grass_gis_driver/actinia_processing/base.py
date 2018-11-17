# -*- coding: utf-8 -*-

# This is the process dictionary that is used to store all processes of the Actinia wrapper
PROCESS_DESCRIPTION_DICT = {}
PROCESS_DICT = {}


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


EXAMPLE_1 = {
    "name": "filter_bands",
    "summary": "Filter an image collection by bands.",
    "description": "Allows to extract one or multiple bands of multi-band raster image "
                   "collection. Bands can be chosen either by band id, band name or by wavelength. "
                   "Imagery and at least one of the other arguments is required to be specified.",
    "min_parameters": 2,
    "parameters":
        {
            "imagery":
                {
                    "description": "EO data to process.",
                    "required": True,
                    "schema": {"type": "object", "format": "eodata"}
                },
            "bands":
                {
                    "description": "string or array of strings containing band ids.",
                    "schema":
                        {
                            "type": ["string", "array"],
                            "items": {"type": "string"}
                        }
                },
            "names":
                {
                    "description": "string or array of strings containing band names.",
                    "schema":
                        {
                            "type": ["string", "array"],
                            "items": {"type": "string"}
                        }
                },
            "wavelengths":
                {
                    "description": "number or two-element array of numbers containing a "
                                   "wavelength or a minimum and maximum wavelength respectively.",
                    "schema":
                        {
                            "type": ["number", "array"],
                            "minItems": 2,
                            "maxItems": 2,
                            "items": {"type": "number"}
                        }
                }
        },
    "returns":
        {
            "description": "Processed EO data.",
            "schema":
                {"type": "object", "format": "eodata"}
        }
}

EXAMPLE_2 = {

    "name": "get_data",
    "summary": "Selects a dataset.",
    "description": "Filters and selects a single dataset provided by the back-end. "
                   "The back-end provider decides which of the potential datasets is "
                   "the most relevant one to be selected.",
    "min_parameters": 1,
    "parameters":
        {
            "data_id":
                {
                    "description": "Filter by data id",
                    "schema":
                        {
                            "type": "string",
                            "examples": ["Sentinel2A-L1C"]
                        }
                },
            "extent":
                {
                    "description": "Filter by extent",
                    "schema":
                        {
                            "type": "object",
                            "required":
                                ["left", "right", "top", "bottom"],
                            "properties":
                                {
                                    "crs":
                                        {
                                            "description": "Coordinate reference system. EPSG codes must be "
                                                           "supported. In addition, proj4 strings should be "
                                                           "supported by back-ends. Whenever possible, it is "
                                                           "recommended to use EPSG codes instead of proj4 "
                                                           "strings. Defaults to `EPSG:4326` unless the client "
                                                           "explicitly requests a different coordinate reference "
                                                           "system.",
                                            "type": "string",
                                            "default": "EPSG:4326"
                                        },
                                    "left": {"type": "number"},
                                    "right": {"type": "number"},
                                    "top": {"type": "number"},
                                    "bottom": {"type": "number"}
                                }
                        }
                },
            "time":
                {
                    "description": "Filter by time",
                    "schema":
                        {"type": "string"}
                },
            "bands":
                {
                    "description": "Filter by band IDs",
                    "schema":
                        {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                },
            "derived_from":
                {
                    "description": "Filter by derived data set",
                    "schema":
                        {
                            "type": ["string",
                                     "null"]
                        }
                },
            "license":
                {
                    "description": "Filter by license",
                    "schema":
                        {
                            "type": "string",
                            "examples": ["Apache-2.0"],
                            "description": "If available, should be a license from the SPDX "
                                           "License List: https://spdx.org/licenses/"
                        }
                }
        },
    "returns":
        {
            "description": "Processed EO data.",
            "schema":
                {
                    "type": "object",
                    "format": "eodata"
                }
        }
}


def analyse_process_graph_legacy(graph):
    """Analyse a process process graph and call the required subprocess analysis

    This function return the list of input names for the next process and the
    Actinia process chain that was build before.

    :param graph: The process description
    :return: (output_name_list, pc)
    """

    if not graph or ("collections" not in graph and "process_graph" not in graph):
        raise Exception("process_graph or collection not found on process description")

    process_list = []
    input_list = []

    if "process_graph" in graph:
        entry = graph["process_graph"]

        if "process_id" in entry:

            if entry["process_id"] not in PROCESS_DICT:
                raise Exception("Unsupported process id")

            inputs, processes = PROCESS_DICT[entry["process_id"]](entry["args"])
            process_list.extend(processes)
            input_list.extend(inputs)
        if "product_id" in entry:
            input = entry["product_id"]
            input_list.append(input)

    elif "collections" in graph:
        entry_list = graph["collections"]
        for entry in entry_list:

            if "process_id" in entry:

                if entry["process_id"] not in PROCESS_DICT:
                    raise Exception("Unsupported process id")

                inputs, processes = PROCESS_DICT[entry["process_id"]](entry["args"])
                process_list.extend(processes)
                input_list.extend(inputs)
            if "product_id" in entry:
                inputs = entry["product_id"]
                input_list.append(inputs)

    return input_list, process_list


def analyse_process_graph(graph):
    """Analyse a process graph and call the required subprocess analysis

    This function return the list of input names for the next process and the
    Actinia process chain that was build before.

    :param graph: The process description
    :return: (output_name_list, process_list)
    """

    if graph is None:
        raise Exception("Empty process graph")

    process_list = []
    output_name_list = []

    for key in graph:
        process = graph[key]

        if "process_id" in process:

            if process["process_id"] not in PROCESS_DICT:
                raise Exception("Unsupported process id, available processes: %s"%PROCESS_DICT.keys())

            outputs, processes = PROCESS_DICT[process["process_id"]](process)
            process_list.extend(processes)
            output_name_list.extend(outputs)

    return output_name_list, process_list
