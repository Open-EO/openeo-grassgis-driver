# -*- coding: utf-8 -*-
from random import randint
import json

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph, ProcessGraphNode

from openeo_grass_gis_driver.actinia_processing.base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node, \
    check_node_parents, DataObject
from openeo_grass_gis_driver.models.process_schemas import Parameter, ProcessDescription, ReturnValue, ProcessExample

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2019, Markus Metz, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

PROCESS_NAME = "load_collection"

# based on get_data, updated to OpenEO API v0.4, then to v1.0

def create_process_description():

    p_data = Parameter(description="The collection identifier.",
                        schema={"type": "string",
                                "subtype": "collection-id",
                                "pattern": "^[A-Za-z0-9_\\-\\.~/]+$",
                                "examples": ["nc_spm_08.landsat.raster.lsat5_1987_10",
                                             "nc_spm_08.PERMANENT.vector.lakes",
                                             "ECAD.PERMANENT.strds.temperature_1950_2017_yearly"]},
                          required=True)
    p_spatial = Parameter(description="Limits the data to load from the collection to the specified bounding box or polygons.\n\n"
                                          "The coordinate reference system of the bounding box must be specified as [EPSG](http://www.epsg.org) code or [PROJ](https://proj4.org) definition.",
                       schema=[{
                                "title": "Bounding Box",
                                "type": "object",
                                "subtype": "bounding-box",
                                "required": [
                                  "west",
                                  "south",
                                  "east",
                                  "north"
                                ],
                                "properties": {
                                  "west": {
                                    "description": "West (lower left corner, coordinate axis 1).",
                                    "type": "number"
                                  },
                                  "south": {
                                    "description": "South (lower left corner, coordinate axis 2).",
                                    "type": "number"
                                  },
                                  "east": {
                                    "description": "East (upper right corner, coordinate axis 1).",
                                    "type": "number"
                                  },
                                  "north": {
                                    "description": "North (upper right corner, coordinate axis 2).",
                                    "type": "number"
                                  },
                                  "base": {
                                    "description": "Base (optional, lower left corner, coordinate axis 3).",
                                    "type": [
                                      "number",
                                      "null"
                                    ],
                                    "default": "null"
                                  },
                                  "height": {
                                    "description": "Height (optional, upper right corner, coordinate axis 3).",
                                    "type": [
                                      "number",
                                      "null"
                                    ],
                                    "default": "null"
                                  },
                                  "crs": {
                                    "description": "Coordinate reference system of the extent, specified as as [EPSG code](http://www.epsg-registry.org/), [WKT2 (ISO 19162) string](http://docs.opengeospatial.org/is/18-010r7/18-010r7.html) or [PROJ definition (deprecated)](https://proj.org/usage/quickstart.html). Defaults to `4326` (EPSG code 4326) unless the client explicitly requests a different coordinate reference system.",
                                    "schema": {
                                      "anyOf": [
                                        {
                                          "title": "EPSG Code",
                                          "type": "integer",
                                          "format": "epsg-code",
                                          "examples": [
                                            7099
                                          ]
                                        },
                                        {
                                          "title": "WKT2",
                                          "type": "string",
                                          "subtype": "wkt2-definition"
                                        },
                                        {
                                          "title": "PROJ definition",
                                          "type": "string",
                                          "subtype": "proj-definition",
                                          "deprecated": "true"
                                        }
                                      ],
                                      "default": 4326
                                    }
                                  }
                                }
                            },
                            {
                              "title": "GeoJSON Polygon(s)",
                              "type": "object",
                              "subtype": "geojson"
                            }
                          ],
                    required=True)
    p_temporal = Parameter(description="Limits the data to load from the collection to the specified left-closed temporal interval. Applies to all temporal dimensions if there are multiple of them. Left-closed temporal interval, i.e. an array with exactly two elements:\n\n1. The first element is the start of the date and/or time interval. The specified instance in time is **included** in the interval.\n2. The second element is the end of the date and/or time interval. The specified instance in time is **excluded** from the interval.\n\nThe specified temporal strings follow [RFC 3339](https://tools.ietf.org/html/rfc3339). Although [RFC 3339 prohibits the hour to be '24'](https://tools.ietf.org/html/rfc3339#section-5.7), **this process allows the value '24' for the hour** of an end time in order to make it possible that left-closed time intervals can fully cover the day.\n\nAlso supports open intervals by setting one of the boundaries to `null`, but never both.",
                       schema={"type": "array",
                               "subtype": "temporal-interval",
                               "minItems": 2,
                               "maxItems": 2,
                               "items": {
                                 "anyOf": [
                                  {
                                    "type": "string",
                                    "format": "date-time",
                                    "subtype": "date-time"
                                  },
                                  {
                                    "type": "string",
                                    "format": "date",
                                    "subtype": "date"
                                  },
                                  {
                                    "type": "string",
                                    "subtype": "time"
                                  },
                                  {
                                    "type": "null"
                                  }
                                ]
                              },
                              "examples": [
                                [
                                  "2015-01-01",
                                  "2016-01-01"
                                ],
                                [
                                  "12:00:00Z",
                                  "24:00:00Z"
                                ]
                              ]
                            },
                       required=True)

    p_bands = Parameter(description="Only adds the specified bands into the data cube so that bands that don't match the list of band names are not available. Applies to all dimensions of type `bands` if there are multiple of them.\n\nThe order of the specified array defines the order of the bands in the data cube.",
                      schema=[
                        {
                          "type": "array",
                          "items": {
                            "type": "string",
                            "subtype": "band-name"
                          }
                        }])
    p_properties = Parameter(description="Limits the data by metadata properties to include only data in the data cube which all given expressions return `true` for (AND operation).\n\nSpecify key-value-pairs with the keys being the name of the metadata property, which can be retrieved with the openEO Data Discovery for Collections. The values must be expressions to be evaluated against the collection metadata, see the example.\n\n**Note:** Back-ends may not pass the actual value to the expressions, but pass a proprietary index or a placeholder so that they can use the expressions to query against another data source. So debugging on the callback parameter `value` may lead to unexpected results.",
              experimental=True,
              schema=[
                {
                  "type": "object",
                  "additionalProperties": {
                  "type": "object",
                  "parameters": {
                  "value": {
                  "description": "The property value. Any data type could be passed."
                  }
                },
                "subtype": "process-graph"
                }
                }])

    rv = ReturnValue(description="Processed EO data.",
                     schema={"type": "object", "subtype": "raster-cube"})

    # Example
    arguments = {"id": "latlong_wgs84.modis_ndvi_global.strds.ndvi_16_5600m",
                 "spatial_extent": {
                      "west": 16.1,
                      "east": 16.6,
                      "north": 48.6,
                      "south": 47.2
                    },
                "temporal_extent": [
                      "2018-01-01",
                      "2019-01-01"
                    ],
                }
    node = ProcessGraphNode(process_id=PROCESS_NAME, arguments=arguments)
    graph = ProcessGraph(title="title", description="description", process_graph={"load_strds_collection": node})
    examples = [ProcessExample(title="Simple example", description="Simple example",
                               process_graph=graph)]

    pd = ProcessDescription(id=PROCESS_NAME,
                            description="Loads a collection from the current back-end by its id and "
                                        "returns it as processable data cube.",
                            summary="Load a collection",
                            parameters={"id": p_data,
                                        "spatial_extent": p_spatial,
                                        "temporal_extent": p_temporal,
                                        "bands": p_bands,
                                        "properties": p_properties
                                        },
                            returns=rv,
                            examples=examples)

    return json.loads(pd.to_json())


PROCESS_DESCRIPTION_DICT[PROCESS_NAME] = create_process_description()



def create_process_chain_entry(input_object: DataObject,
                               spatial_extent,
                               temporal_extent,
                               bands,
                               output_object: DataObject):
    """Create a Actinia process description that r.info, v.info, or t.info.

    :param input_object: The input object name
    :param spatial_extent: spatial filter
    :param temporal_extent: temporal filter
    :param bands: bands to extract
    :return: A Actinia process chain description
    """

    rn = randint(0, 1000000)

    pc = []

    if input_object.is_raster():
        importer = {"id": "r_info_%i" % rn,
              "module": "r.info",
              "inputs": [{"param": "map", "value": input_object.grass_name()}, ],
              "flags": "g"}
    elif input_object.is_vector():
        importer = {"id": "v_info_%i" % rn,
              "module": "v.info",
              "inputs": [{"param": "map", "value": input_object.grass_name()}, ],
              "flags": "g"}
    elif input_object.is_strds():
        importer = {"id": "t_info_%i" % rn,
              "module": "t.info",
              "inputs": [{"param": "input", "value": input_object.grass_name()}, ],
              "flags": "g"}
    else:
        raise Exception("Unsupported datatype")

    pc.append(importer)

    if spatial_extent is not None:
        north = spatial_extent["north"]
        south = spatial_extent["south"]
        west = spatial_extent["west"]
        east = spatial_extent["east"]
        if "crs" in spatial_extent:
            crs = spatial_extent["crs"]
        else:
            crs = "4326"

        if crs.isnumeric():
            crs = "EPSG:" + crs

        if input_object.is_raster():
            region_bbox = {"id": "g_region_bbox_%i" % rn,
                  "module": "g.region.bbox",
                  "inputs": [{"param": "n", "value": str(north)},
                             {"param": "s", "value": str(south)},
                             {"param": "e", "value": str(east)},
                             {"param": "w", "value": str(west)},
                             {"param": "crs", "value": str(crs)},
                             {"param": "raster", "value": input_object.grass_name()},]}
        elif input_object.is_strds():
            region_bbox = {"id": "g_region_bbox_%i" % rn,
                  "module": "g.region.bbox",
                  "inputs": [{"param": "n", "value": str(north)},
                             {"param": "s", "value": str(south)},
                             {"param": "e", "value": str(east)},
                             {"param": "w", "value": str(west)},
                             {"param": "crs", "value": str(crs)},
                             {"param": "strds", "value": input_object.grass_name()},]}
        else:
            region_bbox = {"id": "g_region_bbox_%i" % rn,
                  "module": "g.region.bbox",
                  "inputs": [{"param": "n", "value": str(north)},
                             {"param": "s", "value": str(south)},
                             {"param": "e", "value": str(east)},
                             {"param": "w", "value": str(west)},
                             {"param": "crs", "value": str(crs)},]}

        pc.append(region_bbox)
    
    if input_object.is_strds() and \
       (temporal_extent is not None or bands is not None):
        wherestring = ""
        if temporal_extent:
            start_time = temporal_extent[0].replace('T', ' ')
            end_time = temporal_extent[1].replace('T', ' ')
            # end_time can be null, use only start_time for filtering
            wherestring = "start_time >= '%(start)s' AND start_time <= '%(end)s'" % {"start": start_time, "end": end_time}
            if bands:
                wherestring = wherestring + " AND "
        if bands:
            wherestring = wherestring + "band_reference in ('%(band_names)s')" % {"band_names": ("', '").join(bands)}

        pc_strdsfilter = {"id": "t_rast_extract_%i" % rn,
          "module": "t.rast.extract",
          "inputs": [{"param": "input", "value": input_object.grass_name()},
                     {"param": "where", "value": wherestring},
                     {"param": "output", "value": output_object.grass_name()},
                     {"param": "expression", "value": "1.0 * %s" % input_object.grass_name()},
                     {"param": "basename", "value": f"{input_object.name}_extract"},
                     {"param": "suffix", "value": "num"}]}

        pc.append(pc_strdsfilter)

    return pc


def get_process_list(node: Node):
    """Analyse the process description and return the Actinia process chain and the name of the processing result

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """

    input_objects, process_list = check_node_parents(node=node)
    output_objects = []

    # First analyse the data entry
    if "id" not in node.arguments:
        raise Exception("Process %s requires parameter <data>" % PROCESS_NAME)

    input_object = DataObject.from_string(node.arguments["id"])

    spatial_extent = None
    if "spatial_extent" in node.arguments:
        spatial_extent = node.arguments["spatial_extent"]
    temporal_extent = None
    if "temporal_extent" in node.arguments:
        temporal_extent = node.arguments["temporal_extent"]
    bands = None
    if "bands" in node.arguments:
        bands = node.arguments["bands"]

    if input_object.is_strds() and \
       (temporal_extent is not None or bands is not None):
        output_object = DataObject(name=f"{input_object.name}_{PROCESS_NAME}", datatype=input_object.datatype)
    else:
        output_object = input_object 

    output_objects.append(output_object)
    node.add_output(output_object)
    
    pc = create_process_chain_entry(input_object,
                                    spatial_extent,
                                    temporal_extent,
                                    bands,
                                    output_object)
    process_list.extend(pc)

    return output_objects, process_list


PROCESS_DICT[PROCESS_NAME] = get_process_list
