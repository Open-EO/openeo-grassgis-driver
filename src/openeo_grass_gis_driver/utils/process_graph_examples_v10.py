# -*- coding: utf-8 -*-

__author__ = "Markus Metz"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

GET_DATA_1 = {
    "title": "Get a raster layer",
    "description": "This process is the source for a raster layer",
    "process": {
        "process_graph": {
            "get_elevation_data": {
                "process_id": "load_collection",
                "arguments": {
                    "id": "nc_spm_08.PERMANENT.raster.elevation",
                    "spatial_extent": {
                        "west": 630000,
                        "east": 645000,
                        "north": 228500,
                        "south": 215000,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                    "temporal_extent": [
                        "2018-01-01",
                        "2019-01-01"
                    ],
                }
            }
        }
    }
}

GET_DATA_2 = {
    "title": "Get three different data sources",
    "description": "This process graph is the source for three different layer: raster, vector and strds",
    "process": {
        "process_graph": {
            "get_lakes_data": {
                "process_id": "load_collection",
                "arguments": {
                    "id": "nc_spm_08.PERMANENT.vector.lakes",
                    "spatial_extent": {
                        "west": 610760.703856752,
                        "east": 677118.419100839,
                        "north": 258302.909848466,
                        "south": 196084.815242403,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                    "temporal_extent": [
                        "2018-01-01",
                        "2019-01-01"
                    ],
                }
            },
            "get_elevation_data": {
                "process_id": "load_collection",
                "arguments": {
                    "id": "nc_spm_08.PERMANENT.raster.elevation",
                    "spatial_extent": {
                        "west": 630000,
                        "east": 645000,
                        "north": 228500,
                        "south": 215000,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                    "temporal_extent": [
                        "2018-01-01",
                        "2019-01-01"
                    ],
                }
            }
        }
    }
}

GET_DATA_3 = {
    "title": "Get three different data sources",
    "description": "This process graph is the source for three different layer: raster, vector and strds",
    "process": {
        "process_graph": {
            "get_strds_data": {
                "process_id": "load_collection",
                "arguments": {
                    "id": "nc_spm_08.modis_lst.strds.LST_Day_monthly",
                    "spatial_extent": {
                        "west": -448265.535885,
                        "east": 1550934.464115,
                        "north": 760180.124115,
                        "south": -415819.875885,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                    "temporal_extent": [
                        "2015-01-01",
                        "2017-01-01"
                    ],
                }
            }
        }
    }
}

# bbox_from_raster no longer exists
"""
BBOX_FROM_RASTER = {
    "title": "Bounding box filtering of raster layer elevation",
    "description": "This process graph applies the bounding box filter of a raster layer",
    "process_graph": {
        "bbox_from_raster_1": {
            "process_id": "bbox_from_raster",
            "arguments": {
                "data": {"from_node": "get_data_1"}
            }
        },
        "get_data_1": {
            "process_id": "load_collection",
            "arguments": {
                "id":  "nc_spm_08.PERMANENT.raster.elevation",
                "spatial_extent": {
                    "west": 630000,
                    "east": 645000,
                    "north": 228500,
                    "south": 215000,
                    "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                "temporal_extent": [
                    "2018-01-01",
                    "2019-01-01"
                    ],
            }
        }
    }
}
"""

FILTER_BBOX = {
    "title": "Bounding box filtering of raster layer elevation",
    "description": "This process graph applies the bounding box filter to a raster layer",
    "process": {
        "process_graph": {
            "filter_bbox_1": {
                "process_id": "filter_bbox",
                "arguments": {
                    "data": {"from_node": "get_data_1"},
                    "extent": {
                        "west": 630000,
                        "east": 645000,
                        "north": 228500,
                        "south": 215000,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +to_meter=1",
                    }
                }
            },
            "get_data_1": {
                "process_id": "load_collection",
                "arguments": {
                    "id": "nc_spm_08.PERMANENT.raster.elevation",
                    "spatial_extent": {
                        "west": 630000,
                        "east": 645000,
                        "north": 228500,
                        "south": 215000,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                    "temporal_extent": [
                        "2018-01-01",
                        "2019-01-01"
                    ],
                }
            }
        }
    }
}

DATERANGE = {
    "title": "Filter the daterange of a single STRDS",
    "description": "Filter the daterange of a single STRDS",
    "process": {
        "process_graph": {
            "get_strds_data": {
                "process_id": "load_collection",
                "arguments": {
                    "id": "nc_spm_08.modis_lst.strds.LST_Day_monthly",
                    "spatial_extent": {
                        "west": -448265.535885,
                        "east": 1550934.464115,
                        "north": 760180.124115,
                        "south": -415819.875885,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                    "temporal_extent": [
                        "2015-01-01",
                        "2017-01-01"
                    ],
                }
            },
            "filter_daterange_1": {
                "process_id": "filter_temporal",
                "arguments": {
                    "data": {"from_node": "get_strds_data"},
                    "extent": ["2015-01-01", "2016-01-01"],
                }
            }
        }
    }
}

REDUCE_TIME_MIN = {
    "title": "Reduce the time dimension of a single STRDS",
    "description": "Reduce the time dimension of a single STRDS",
    "process": {
        "process_graph": {
            "get_strds_data": {
                "process_id": "load_collection",
                "arguments": {
                    "id": "nc_spm_08.modis_lst.strds.LST_Day_monthly",
                    "spatial_extent": {
                        "west": -448265.535885,
                        "east": 1550934.464115,
                        "north": 760180.124115,
                        "south": -415819.875885,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                    "temporal_extent": [
                        "2015-01-01",
                        "2017-01-01"
                    ],
                }
            },
            "reduce_time_1": {
                "process_id": "reduce_dimension",
                "arguments": {
                    "data": {"from_node": "get_strds_data"},
                    "dimension": "temporal",
                    "reducer": {
                        "process_graph": {
                            "min1": {
                                "process_id": "min",
                                "arguments": {
                                    "data": {
                                        "from_argument": "data"
                                    },
                                    "dimension": {
                                        "from_argument": "dimension"
                                    }
                                },
                                "result": True
                            }
                        }
                    }
                }
            }
        }
    }
}

# map_algebra no longer exists
# TODO: replace with reduce_dimension
"""
MAP_ALGEBRA = {
    "title": "Compute the NDVI based on two raster layers with map algebra",
    "description": "Compute the NDVI based on two raster layers with map algebra",
    "process_graph": {
        "mapcalc_1": {
            "process_id": "map_algebra",
            "arguments": {
                "a": {"from_node": "get_red_data"},
                "b": {"from_node": "get_nir_data"},
                "result": "ndvi",
                "expression": "$result = ($a + $b / ($a - $b))"
            }
        },
        "get_red_data": {
            "process_id": "load_collection",
            "arguments": {
                "id":  "nc_spm_08.landsat.raster.lsat7_2000_30",
                "spatial_extent": {
                    "west": 629992.5,
                    "east": 645012,
                    "north": 228513,
                    "south": 214975.5,
                    "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                "temporal_extent": [
                    "2015-01-01",
                    "2017-01-01"
                    ],
            }
        },
        "get_nir_data": {
            "process_id": "load_collection",
            "arguments": {
                "id":  "nc_spm_08.landsat.raster.lsat7_2000_40",
                "spatial_extent": {
                    "west": 629992.5,
                    "east": 645012,
                    "north": 228513,
                    "south": 214975.5,
                    "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                "temporal_extent": [
                    "2015-01-01",
                    "2017-01-01"
                    ],
            }
        }
    }
}
"""

# temporal_algebra no longer exists
# TODO: replace with reduce_dimension
"""
TEMPORAL_ALGEBRA = {
    "title": "Compute the NDVI based on two strds with temporal algebra",
    "description": "Compute the NDVI based on two strds with temporal algebra",
    "process_graph": {
        "talgebra_1": {
            "process_id": "temporal_algebra",
            "arguments": {
                "a": {"from_node": "get_red_data"},
                "b": {"from_node": "get_nir_data"},
                "result": "ndvi",
                "basename": "ndvi_base",
                "expression": "$result = ($a + $b / ($a - $b))"
            }
        },
        "get_red_data": {
            "process_id": "load_collection",
            "arguments": {
                "id":  "nc_spm_08.landsat.strds.lsat5_1987_30",
                "spatial_extent": {
                    "west": 629992.5,
                    "east": 645012,
                    "north": 228513,
                    "south": 214975.5,
                    "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                "temporal_extent": [
                    "1987-01-01",
                    "1988-01-01"
                    ],
            }
        },
        "get_nir_data": {
            "process_id": "load_collection",
            "arguments": {
                "id":  "nc_spm_08.landsat.strds.lsat5_1987_40",
                "spatial_extent": {
                    "west": 629992.5,
                    "east": 645012,
                    "north": 228513,
                    "south": 214975.5,
                    "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                "temporal_extent": [
                    "1987-01-01",
                    "1988-01-01"
                    ],
            }
        }
    }
}
"""

# rgb_raster_exporter does not exist
"""
RGB_RASTER_EXPORT = {
    "title": "Export three raster maps as RGB composite",
    "description": "Export three raster maps as RGB composite",
    "process_graph": {
        "rgb_raster_exporter_1": {
            "process_id": "rgb_raster_exporter",
            "arguments": {
                "red": {"from_node": "bbox_from_raster_red"},
                "green": {"from_node": "get_green_data"},
                "blue": {"from_node": "get_blue_data"},
            }
        },
        "bbox_from_raster_red": {
            "process_id": "bbox_from_raster",
            "arguments": {
                "data": {"from_node": "get_red_data"}
            }
        },
        "get_red_data": {
            "process_id": "load_collection",
            "arguments": {
                "id":  "nc_spm_08.landsat.raster.lsat7_2000_30",
                "spatial_extent": {
                    "west": 629992.5,
                    "east": 645012,
                    "north": 228513,
                    "south": 214975.5,
                    "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                "temporal_extent": [
                    "2015-01-01",
                    "2017-01-01"
                    ],
            }
        },
        "get_green_data": {
            "process_id": "load_collection",
            "arguments": {
                "id":  "nc_spm_08.landsat.raster.lsat7_2000_20",
                "spatial_extent": {
                    "west": 629992.5,
                    "east": 645012,
                    "north": 228513,
                    "south": 214975.5,
                    "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                "temporal_extent": [
                    "2015-01-01",
                    "2017-01-01"
                    ],
            }
        },
        "get_blue_data": {
            "process_id": "load_collection",
            "arguments": {
                "id":  "nc_spm_08.landsat.raster.lsat7_2000_10",
                "spatial_extent": {
                    "west": 629992.5,
                    "east": 645012,
                    "north": 228513,
                    "south": 214975.5,
                    "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                "temporal_extent": [
                    "2015-01-01",
                    "2017-01-01"
                    ],
            }
        }
    }
}
"""

NDVI_STRDS = {
    "title": "Compute the NDVI based on two STRDS",
    "description": "Compute the NDVI data from two space-time raster datasets",
    "process": {
        "process_graph": {
            "ndvi_1": {
                "process_id": "ndvi",
                "arguments": {
                    "data": {"from_node": "get_data"},
                }
            },
            "get_data": {
                "process_id": "load_collection",
                "arguments": {
                    "id": "nc_spm_08.landsat.strds.lsat5_1987",
                    "spatial_extent": {
                        "west": 629992.5,
                        "east": 645012,
                        "north": 228513,
                        "south": 214975.5,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                    "temporal_extent": [
                        "1987-01-01",
                        "1988-01-01"
                    ],
                }
            }
        }
    }
}

# raster_exporter does not exist
"""
RASTER_EXPORT = {
    "title": "Export the raster data from a single source",
    "description": "Export raster the data from a single source",
    "process_graph": {
        "raster_exporter_1": {
            "process_id": "raster_exporter",
            "arguments": {
                "data": {"from_node": "get_b08_data"}
            }
        },
        "get_b08_data": {
            "process_id": "load_collection",
            "arguments": {
                "id": "nc_spm_08.PERMANENT.raster.elevation",
                "spatial_extent": {
                    "west": 630000,
                    "east": 645000,
                    "north": 228500,
                    "south": 215000,
                    "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                "temporal_extent": [
                    "2018-01-01",
                    "2019-01-01"
                    ],
            }
        }
    }
}
"""

# zonal_statistics does not exist
# TODO: replace with aggregate_spatial
"""
ZONAL_STATISTICS = {
    "title": "Compute zonal statistics based on a strds and a vector layer",
    "description": "Compute zonal statistics based on a strds and a vector layer",
    "process_graph": {
        "zonal_statistics_1": {
            "process_id": "zonal_statistics",
            "arguments": {
                "data": {"from_node": "get_b08_data"},
                "polygons": "https://storage.googleapis.com/graas-geodata/roi_openeo_use_case_2.geojson"
            }
        },
        "get_b08_data": {
            "process_id": "load_collection",
            "arguments": {
                "id": "nc_spm_08.modis_lst.strds.LST_Day_monthly",
                "spatial_extent": {
                    "west": -448265.535885,
                    "east": 1550934.464115,
                    "north": 760180.124115,
                    "south": -415819.875885,
                    "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                "temporal_extent": [
                    "2015-01-01",
                    "2017-01-01"
                    ],
            }
        }
    }
}
"""

USE_CASE_1 = {
    "title": "Compute the NDVI based on two STRDS",
    "description": "Compute the NDVI data from two space-time raster datasets and apply several filters in the data",
    "process": {
        "process_graph": {
            "get_data": {
                "process_id": "load_collection",
                "arguments": {
                    "id": "nc_spm_08.landsat.strds.lsat5_1987",
                    "spatial_extent": {
                        "west": 629992.5,
                        "east": 645012,
                        "north": 228513,
                        "south": 214975.5,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                    "temporal_extent": [
                        "1987-01-01",
                        "1988-01-01"
                    ],
                }
            },
            "filter_bbox": {
                "process_id": "filter_bbox",
                "arguments": {
                    "data": {"from_node": "get_data"},
                    "extent": {
                        "west": 630000,
                        "east": 645000,
                        "north": 228500,
                        "south": 215000,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +to_meter=1",
                    }
                }
            },
            "ndvi_1": {
                "process_id": "ndvi",
                "arguments": {
                    "data": {"from_node": "filter_bbox"},
                }
            },
            "filter_daterange_ndvi": {
                "process_id": "filter_temporal",
                "arguments": {
                    "data": {"from_node": "ndvi_1"},
                    "extent": ["2001-01-01", "2005-01-01"],
                }
            },
            "reduce_time_1": {
                "process_id": "reduce_dimension",
                "arguments": {
                    "data": {"from_node": "filter_daterange_ndvi"},
                    "dimension": "temporal",
                    "reducer": {
                        "process_graph": {
                            "min1": {
                                "process_id": "min",
                                "arguments": {
                                    "data": {
                                        "from_argument": "data"
                                    },
                                    "dimension": {
                                        "from_argument": "dimension"
                                    }
                                },
                                "result": True
                            }
                        }
                    }
                }
            }
        }
    }
}

# export does not exist
OPENEO_EXAMPLE_1 = {
    "title": "NDVI based on Sentinel 2",
    "description": "Deriving minimum NDVI measurements over pixel time series of Sentinel 2",
    "process": {
        "process_graph": {
            "export1": {
                "process_id": "export",
                "arguments": {
                    "data": {
                        "from_node": "mergec1"
                    },
                    "format": "png"
                }
            },
            "export2": {
                "process_id": "export",
                "arguments": {
                    "data": {
                        "from_node": "reduce2"
                    },
                    "format": "png"
                },
                "result": True
            },
            "filter1": {
                "process_id": "filter_temporal",
                "arguments": {
                    "data": {
                        "from_node": "getcol1"
                    },
                    "extent": ["2017-01-01", "2017-01-31"]
                }
            },
            "filter2": {
                "process_id": "filter_temporal",
                "arguments": {
                    "data": {
                        "from_node": "getcol1"
                    },
                    "extent": ["2018-01-01", "2018-01-31"]
                }
            },
            "filter3": {
                "process_id": "filter_bands",
                "arguments": {
                    "bands": [
                        "nir",
                        "red"
                    ],
                    "data": {
                        "from_node": "reduce1"
                    }
                }
            },
            "getcol1": {
                "process_id": "get_collection",
                "arguments": {
                    "name": "Sentinel-1"
                }
            },
            "mergec1": {
                "process_id": "merge_cubes",
                "arguments": {
                    "data1": {
                        "from_node": "filter1"
                    },
                    "data2": {
                        "from_node": "filter2"
                    }
                }
            },
            "reduce1": {
                "process_id": "reduce_dimension",
                "arguments": {
                    "data": {
                        "from_node": "mergec1"
                    },
                    "dimension": "temporal",
                    "reducer": {
                        "process_graph": {
                            "min1": {
                                "process_id": "min",
                                "arguments": {
                                    "data": {
                                        "from_argument": "data"
                                    },
                                    "dimension": {
                                        "from_argument": "dimension"
                                    }
                                },
                                "result": True
                            }
                        }
                    }
                }
            },
            "reduce2": {
                "process_id": "reduce_dimension",
                "arguments": {
                    "data": {
                        "from_node": "filter3"
                    },
                    "dimension": "spectral",
                    "reducer": {
                        "process_graph": {
                            "divide1": {
                                "process_id": "divide",
                                "arguments": {
                                    "x": {
                                        "from_node": "substr1"
                                    },
                                    "y": {
                                        "from_node": "sum1"
                                    }
                                },
                                "result": True
                            },
                            "output1": {
                                "process_id": "output",
                                "arguments": {
                                    "data": {
                                        "from_node": "divide1"
                                    }
                                }
                            },
                            "substr1": {
                                "process_id": "subtract",
                                "arguments": {
                                    "data": {
                                        "from_argument": "dimension_data"
                                    }
                                }
                            },
                            "sum1": {
                                "process_id": "sum",
                                "arguments": {
                                    "data": {
                                        "from_argument": "dimension_data"
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}

ACTINIA_PROCESS = {
    "title": "Get a raster layer",
    "description": "This process is the source for a raster layer",
    "process": {
        "process_graph": {
            "get_elevation_data": {
                "process_id": "load_collection",
                "arguments": {
                    "id": "nc_spm_08.PERMANENT.raster.elevation",
                    "spatial_extent": {
                        "west": 630000,
                        "east": 645000,
                        "north": 228500,
                        "south": 215000,
                        "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +type=crs  +to_meter=1"
                    },
                    "temporal_extent": [
                        "2018-01-01",
                        "2019-01-01"
                    ],
                }
            },
            "compute_slope": {
                "process_id": "r.slope.aspect",
                "arguments": {
                    "elevation": {"from_node": "get_elevation_data"},
                    "e": True,
                    "slope": True,
                }
            }
        }
    }
}
