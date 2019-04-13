# -*- coding: utf-8 -*-
from random import randint
import json
from openeo_grass_gis_driver.actinia_processing.base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.process_schemas import Parameter, ProcessDescription, ReturnValue
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "reduce_time"


def create_process_description():
    p_imagery = Parameter(description="Any openEO process object that returns raster datasets "
                                      "or space-time raster dataset",
                          schema={"type": "object", "format": "eodata"},
                          required=True)

    p_method = Parameter(description="The method to reduce the time dimension of a "
                                     "space-time raster dataset",
                         schema={"type": "string"},
                         required=True)

    p_method.enum = ["average", "count", "median", "mode", "minimum", "min_raster", "maximum",
                     "max_raster", "stddev", "range,sum", "variance", "diversity", "slope",
                     "offset", "detcoeff", "quart1", "quart3", "perc90", "quantile", "skewness",
                     "kurtosis"]

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    simple_example = {
        "process_id": PROCESS_NAME,
        "method": "average",
        "imagery": {
            "process_id": "get_data",
            "data_id": "ECAD.PERMANENT.strds.temperature_1950_2017_yearly"
        }
    }

    examples = dict(simple_example=simple_example)

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Reduce the time dimension of a space-time raster dataset "
                                        "with different reduce options.",
                            summary="Reduce the time dimension of a space-time raster dataset.",
                            parameters={"imagery": p_imagery, "method": p_method},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_name, method, output_name):
    """Create a Actinia process description that uses t.rast.series to reduce a time series.

    :param input_time_series: The input time series name
    :param method: The method for time reduction
    :param output_map: The name of the output map
    :return: A Actinia process chain description
    """
    input_name = ActiniaInterface.layer_def_to_grass_map_name(input_name)

    rn = randint(0, 1000000)

    pc = {"id": "t_rast_series_%i" % rn,
          "module": "t.rast.series",
          "inputs": [{"param": "input", "value": input_name},
                     {"param": "method", "value": method},
                     {"param": "output", "value": output_name}],
          "flags": "t"}

    return pc


def get_process_list(process):
    """Analyse the process description and return the Actinia process chain
    and the name of the processing result layer
    which is a single raster layer

    :param args: The process description arguments
    :return: (output_names, actinia_process_list)
    """
    input_names, process_list = process_node_to_actinia_process_chain(process)
    output_names = []

    if "method" not in process:
        raise Exception("Parameter method is required.")

    for input_name in input_names:
        location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
        output_name = "%s_%s" % (layer_name, PROCESS_NAME)
        output_names.append(output_name)

        pc = create_process_chain_entry(input_name, process["method"], output_name)
        process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
