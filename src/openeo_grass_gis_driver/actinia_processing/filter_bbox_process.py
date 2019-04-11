# -*- coding: utf-8 -*-
import json
from random import randint
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue
from .base import process_node_to_actinia_process_chain, PROCESS_DICT, PROCESS_DESCRIPTION_DICT

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "filter_bbox"


def create_process_description():
    p_imagery = Parameter(description="Any openEO process object that returns raster datasets "
                                      "or space-time raster dataset",
                          schema={"type": "object", "format": "eodata"},
                          required=True)

    extent_schema = {
        "type": "object",
        "required":
            ["left", "right", "top", "bottom", "width_res", "height_res"],
        "properties":
            {
                "left": {"type": "number"},
                "right": {"type": "number"},
                "top": {"type": "number"},
                "bottom": {"type": "number"},
                "width_res": {"type": "number"},
                "height_res": {"type": "number"}
            }
    }

    p_extent = Parameter(description="Filter by spatial extent",
                         schema=extent_schema,
                         required=True)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "format": "eodata"})

    examples = dict(simple={
        "process_id": PROCESS_NAME,
        "imagery": {
            "process_id": "get_data",
            "data_id": "ECAD.PERMANENT.strds.temperature_1950_2017_yearly"
        },
        "spatial_extent": {
            "left": 50,
            "right": 55,
            "top": 60,
            "bottom": 55,
            "width_res": 1,
            "height_res": 1
        }})

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Drops observations from raster data or raster time series data "
                                        " that are located outside of a given bounding box.",
                            summary="Filter raster based data by bounding box",
                            parameters={"imagery": p_imagery, "spatial_extent": p_extent},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(left: float, right: float, top:float,
                               bottom: float, width_res: float, height_res: float) -> dict:
    """Create a Actinia command of the process chain that uses g.region to create a valid computational region
    for the provide input strds

    TODO: This approach is a hack, the g.region command should accept a STRDS as input to set the
          resolution accordingly, or this function must have the resolution option set by the user.

    :param left:
    :param right:
    :param top:
    :param bottom:
    :param width_res:
    :param height_res:
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    pc = {"id": "g_region_%i" % rn,
          "module": "g.region",
          "inputs": [{"param": "n", "value": str(top)},
                     {"param": "s", "value": str(bottom)},
                     {"param": "e", "value": str(right)},
                     {"param": "w", "value": str(left)},
                     {"param": "ewres", "value": str(width_res)},
                     {"param": "nsres", "value": str(height_res)}]}

    return pc


def get_process_list(process):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param process: The process description
    :return: (output_names, actinia_process_list)
    """

    input_names, process_list = process_node_to_actinia_process_chain(process)
    output_names = []

    if "spatial_extent" not in process.keys():
        raise Exception("Process %s requires parameter <spatial_extent>" % PROCESS_NAME)

    if "left" not in process["spatial_extent"] or \
            "right" not in process["spatial_extent"] or \
            "top" not in process["spatial_extent"] or \
            "bottom" not in process["spatial_extent"] or \
            "width_res" not in process["spatial_extent"] or \
            "height_res" not in process["spatial_extent"]:
        raise Exception("Process %s requires parameter left, right, top, bottom, "
                        "width_res, height_res" % PROCESS_NAME)

    left = process["spatial_extent"]["left"]
    right = process["spatial_extent"]["right"]
    top = process["spatial_extent"]["top"]
    bottom = process["spatial_extent"]["bottom"]
    width_res = process["spatial_extent"]["width_res"]
    height_res = process["spatial_extent"]["height_res"]

    pc = create_process_chain_entry(left=left, right=right, top=top,
                                    bottom=bottom, width_res=width_res,
                                    height_res=height_res)
    process_list.append(pc)

    for input_name in input_names:
        # Create the output name based on the input name and method
        output_name = input_name
        output_names.append(output_name)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
