# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraphNode, ProcessGraph

from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, \
    PROCESS_DESCRIPTION_DICT, Node, check_node_parents, DataObject
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "zonal_statistics"


def create_process_description():
    p_data = Parameter(description="Any openEO process object that returns raster datasets "
                       "or space-time raster dataset",
                       schema={"type": "object", "subtype": "raster-cube"},
                       optional=False)

    p_polygons = Parameter(description="URL to a publicly accessible polygon file readable by OGR",
                           schema={"type": "string"},
                           optional=False)

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {"data": {"from_node": "get_b08_data"},
                 "polygons": "https://storage.googleapis.com/graas-geodata/roi_openeo_use_case_2.geojson"}
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"zonal_statistics_1": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Compute the zonal statistics of a time series using a vector polygon. "
                                        "The following parameters are computed: "
                                        "mean, min, max, mean_of_abs, stddev, variance, "
                                        "coeff_var, sum, null_cells, cells",
                            summary="Compute the zonal statistics of a time series using a vector polygon.",
                            parameters={"data": p_data, "polygons": p_polygons},
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()


def create_process_chain_entry(input_object: DataObject, polygons: str):
    """Create a Actinia command of the process chain that computes the regional statistics based on a
    strds and a polygon.

    The computational region will be set to the vector map, the previous region will be saved and after processing
    restored. A mask will be set that uses the vector file as input. This mask will be removed in the end.

    :param input_object: The name of the strds
    :param polygons: The URL to the vector file that defines the regions of interest
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)
    pc = []

    importer = {
        "id": "importer_%i" % rn,
        "module": "importer",
        "inputs": [{
            "import_descr": {
                "source": polygons,
                "type": "vector"
            },
            "param": "map",
            "value": "polygon"
        }]
    }

    g_region_1 = {
        "id": "g_region_1_%i" % rn,
        "module": "g.region",
        "inputs": [{"param": "save",
                    "value": "previous_region"}],
        "flags": "g"}

    g_region_2 = {
        "id": "g_region_2_%i" % rn,
        "module": "g.region",
        "inputs": [{"param": "vector",
                    "value": "polygon"}],
        "flags": "g"}

    r_mask_1 = {
        "id": "r_mask_1_%i" % rn,
        "module": "r.mask",
        "inputs": [{"param": "vector",
                    "value": "polygon"}]
    }

    t_rast_univar = {
        "id": "t_rast_univar_%i" % rn,
        "module": "t.rast.univar",
        "inputs": [{"param": "input",
                    "value": input_object.grass_name()}]
    }

    r_mask_2 = {
        "id": "r_mask_2_%i" % rn,
        "module": "r.mask",
        "flags": "r"
    }

    g_region_3 = {
        "id": "g_region_3_%i" % rn,
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


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result layer
    which is a single raster layer

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    for input_object in input_objects:

        output_objects.append(input_object)
        node.add_output(output_object=input_object)

        if "polygons" in node.arguments:
            polygons = node.arguments["polygons"]
        else:
            raise Exception("The vector polygon is missing in the process description")

        pc = create_process_chain_entry(input_object=input_object,
                                        polygons=polygons)
        process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
