# -*- coding: utf-8 -*-
from graas_openeo_core_wrapper import process_definitions
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from random import randint

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
            "description": "left boundary (longitude / easting)"
        },
        "right": {
            "description": "right boundary (longitude / easting)"
        },
        "top": {
            "description": "top boundary (latitude / northing)"
        },
        "bottom": {
            "description": "bottom boundary (latitude / northing)"
        },
        "srs": {
            "description": "spatial reference system of boundaries as proj4 or EPSG:12345 like string"
        }
    }
}

process_definitions.PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_graas_process_chain_entry(strds_name, left=None, right=None, top=None, bottom=None):
    """Create a GRaaS command of the process chain that uses g.region to create a valid computational region
    for the provide input strds

    :param strds_name: The name of the strds
    :param left:
    :param right:
    :param top:
    :param bottom:
    :return: A GRaaS process chain description
    """
    iface = GRaaSInterface()

    # Check for mapset definition, default is PERMANENT

    mapset = "PERMANENT"
    if "@" in strds_name:
        strds_name, mapset = strds_name.split("@")

    # Get region information about the required strds
    status_code, strds_info = iface.strds_info(mapset=mapset, strds_name=strds_name)

    if status_code != 200:
        raise Exception("Unable to get strds info for %s. Response: %s"%(strds_name, strds_info))

    ewres = strds_info["ewres_min"]
    nsres = strds_info["nsres_min"]

    if left is None:
        left = strds_info["west"]
    if right is None:
        right = strds_info["east"]
    if top is None:
        top = strds_info["north"]
    if bottom is None:
        bottom = strds_info["south"]

    # Get info about the time series to extract its resolution settings and bbox

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
    """Analyse the process description and return the GRaaS process chain and the name of the processing result layer
    which is a single raster layer

    :param args: The process description
    :return: (output_name, pc)
    """

    # Get the input description and the process chain to attach this process
    input_names, process_list = process_definitions.analyse_process_graph(args)

    # Pipe the input name to the output
    output_name = input_names[0]

    left = None
    right = None
    top = None
    bottom = None

    if "left" in args:
        left = args["left"]
    if "right" in args:
        right = args["right"]
    if "top" in args:
        top = args["top"]
    if "bottom" in args:
        bottom = args["bottom"]

    if "srs" in args:
        print("SRS is currently not supported")

    pc = create_graas_process_chain_entry(strds_name=input_names[0], left=left, right=right, top=top, bottom=bottom)
    process_list.append(pc)

    return [output_name,], process_list


process_definitions.PROCESS_DICT[PROCESS_NAME] = get_process_list
