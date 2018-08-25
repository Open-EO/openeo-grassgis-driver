# -*- coding: utf-8 -*-
from random import randint
from . import analyse_process_graph, PROCESS_DICT, PROCESS_DESCRIPTION_DICT
from .actinia_interface import ActiniaInterface

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


PROCESS_NAME = "zonal_statistics"

DOC = {
    "process_id": PROCESS_NAME,
    "description": "Compute the zonal statistics of a time series using a vector polygon. "
                   "The following parameters are computed: "
                   "mean, min, max, mean_of_abs, stddev, variance, coeff_var, sum, null_cells, cells",
    "args": {
        "imagery": {
            "description": "array of input collections with at least one element that must be of type time series"
        },
        "regions": {
            "description": "URL to a publicly accessible polygon file readable by OGR"
        }
    }
}

PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = DOC


def create_process_chain_entry(input_name, regions):
    """Create a GRaaS command of the process chain that computes the regional statistics based on a
    strds and a polygon.

    The computational region will be set to the vector map, the previous region will be saved and after processing
    restored. A mask will be set that uses the vector file as input. This mask will be removed in the end.

    :param input_name: The name of the strds
    :param regions: The URL to the vector file that defines the regions of interest
    :return: A GRaaS process chain description
    """

    location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(input_name)
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

    g_region_1 = {
        "id": "g_region_%i" % rn,
        "module": "g.region",
        "inputs": [{"param": "save",
                    "value": "previous_region"}],
        "flags": "g"}

    g_region_2 = {
        "id": "g_region_%i" % rn,
        "module": "g.region",
        "inputs": [{"param": "vector",
                    "value": "polygon"}],
        "flags": "g"}

    r_mask_1 = {
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

    r_mask_2 = {
        "id": "r_mask_%i" % rn,
        "module": "r.mask",
        "flags": "r"
    }

    g_region_3 = {
        "id": "g_region_%i" % rn,
        "module": "g.region",
        "inputs": [{"param": "region",
                    "value": "previous_region"}],
        "flags": "g"}

    pc.append(importer)
    pc.append(g_region_1)
    pc.append(g_region_2)
    pc.append(r_mask_1)
    pc.append(t_rast_univar)
    pc.append(r_mask_2)
    pc.append(g_region_3)

    return pc


def get_process_list(args):
    """Analyse the process description and return the GRaaS process chain and the name of the processing result layer
    which is a single raster layer

    :param args: The process description
    :return: (output_name, pc)
    """

    # Get the input description and the process chain to attach this process
    input_names, process_list = analyse_process_graph(args)
    output_names = []

    for input_name in input_names:

        output_name = input_name
        output_names.append(output_name)

        if "regions" in args:
            regions = args["regions"]
        else:
            raise Exception("The vector polygon is missing in the process description")

        pc = create_process_chain_entry(input_name=input_name,
                                              regions=regions)
        process_list.extend(pc)

    return output_names, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
