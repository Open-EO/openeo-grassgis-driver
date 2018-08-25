# -*- coding: utf-8 -*-
from random import randint
from . import analyse_process_graph, PROCESS_DICT, PROCESS_DESCRIPTION_DICT

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


PROCESS_NAME = "filter_bbox"

DOC = {
    "process_id": PROCESS_NAME,
    "description": "Drops observations from a collection that are located outside of a given bounding box.",
    "args": {
        "collections": {
            "description": "array of input collections with one element"
        },
        "left": {
            "description": "left boundary (longitude / easting)",
            "required":True
        },
        "right": {
            "description": "right boundary (longitude / easting)",
            "required":True
        },
        "top": {
            "description": "top boundary (latitude / northing)",
            "required":True
        },
        "bottom": {
            "description": "bottom boundary (latitude / northing)",
            "required":True
        },
        "ewres": {
            "description": "East-west resolution in mapset units",
            "required":True
        },
        "nsres": {
            "description": "North-south resolution in mapset units",
            "required":True
        },
        "srs": {
            "description": "spatial reference system of boundaries as proj4 or EPSG:12345 like string"
        }
    }
}

PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_process_chain_entry(left, right, top, bottom, ewres, nsres):
    """Create a GRaaS command of the process chain that uses g.region to create a valid computational region
    for the provide input strds

    TODO: This approach is a hack, the g.region command should accept a STRDS as input to set the
          resolution accordingly, or this function must have the resolution option set by the user.

    :param left:
    :param right:
    :param top:
    :param bottom:
    :param ewres:
    :param nsres:
    :return: A GRaaS process chain description
    """

    rn = randint(0, 1000000)

    pc = {"id": "g_region_%i"%rn,
          "module": "g.region",
          "inputs": [{"param": "n", "value": str(top)},
                     {"param": "s", "value": str(bottom)},
                     {"param": "e", "value": str(right)},
                     {"param": "w", "value": str(left)},
                     {"param": "ewres", "value": str(ewres)},
                     {"param": "nsres", "value": str(nsres)}]}

    return pc


def get_process_list(args):
    """Analyse the process description and return the GRaaS process chain and the name of the processing result

    :param args: The process description
    :return: (output_name, pc)
    """

    input_names, process_list = analyse_process_graph(args)
    output_names = []

    for input_name in input_names:

        # Create the output name based on the input name and method
        output_name = input_name
        output_names.append(output_name)

        left = args["left"]
        right = args["right"]
        top = args["top"]
        bottom = args["bottom"]
        ewres = args["ewres"]
        nsres = args["nsres"]

        if "srs" in args:
            print("SRS is currently not supported")

        pc = create_process_chain_entry(left=left, right=right, top=top, bottom=bottom, ewres=ewres, nsres=nsres)
        process_list.append(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
