# -*- coding: utf-8 -*-
from graas_openeo_core_wrapper import process_definitions
from graas_openeo_core_wrapper.graas_interface import GRaaSInterface
from random import randint

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "zonal_statistics"

DOC = {
    "process_id": PROCESS_NAME,
    "description": "Runs a Python script for each time series of the input dataset.",
    "args": {
        "imagery": {
            "description": "array of input collections with one element"
        },
        "regions": {
            "description": "URL to a publicly downloadable Polygon file readable by OGR"
        }
    }
}

process_definitions.PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_graas_process_chain_entry(input_name, regions):
    """Create a GRaaS command of the process chain that computes the regional statistics based on a
    strds and a polygon.

    :param input_name: The name of the strds
    :param regions: The URL to the vector file that defines the regions of interest
    :return: A GRaaS process chain description
    """

    location, mapset, datatype, layer_name = GRaaSInterface.layer_def_to_components(input_name)
    input_name = layer_name
    if mapset is not None:
        input_name = layer_name + "@" + mapset

    rn = randint(0, 1000000)
    pc = []

    importer = {
        "id": "importer_%i" % rn,
        "module": "importer",
        "inputs": [{
            "import_descr": {
                "source": regions,
                "type": "vector"
            },
            "param": "map",
            "value": "polygon"
        }]
    }

    g_region = {
        "id": "g_region_%i" % rn,
        "module": "g.region",
        "inputs": [{"param": "vector",
                    "value": "polygon"}],
        "flags": "g"}

    r_mask = {
        "id": "r_mask_%i" % rn,
        "module": "r.mask",
        "inputs": [{"param": "vector",
                    "value": "polygon"}]
    }

    t_rast_univar = {
        "id": "t_rast_univar_%i" % rn,
        "module": "t.rast.univar",
        "inputs": [{"param": "input",
                    "value": input_name}]
    }

    pc.append(importer)
    pc.append(g_region)
    pc.append(r_mask)
    pc.append(t_rast_univar)

    return pc


def get_process_list(args):
    """Analyse the process description and return the GRaaS process chain and the name of the processing result layer
    which is a single raster layer

    :param args: The process description
    :return: (output_name, pc)
    """

    # Get the input description and the process chain to attach this process
    input_names, process_list = process_definitions.analyse_process_graph(args)
    output_names = []

    for input_name in input_names:

        output_name = input_name
        output_names.append(output_name)

        if "regions" in args:
            regions = args["regions"]
        else:
            raise Exception("The vector polygon is missing in the process description")

        pc = create_graas_process_chain_entry(input_name=input_name,
                                              regions=regions)
        process_list.append(pc)

    return output_names, process_list


process_definitions.PROCESS_DICT[PROCESS_NAME] = get_process_list
