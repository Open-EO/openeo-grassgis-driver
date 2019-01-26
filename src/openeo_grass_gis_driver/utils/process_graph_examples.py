# -*- coding: utf-8 -*-

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

GET_DATA_1 = {
    "title": "Get a raster layer",
    "description": "This process is the source for a raster layer",
    "process_graph": {
        "get_elevation_data": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "nc_spm_08.PERMANENT.raster.elevation"
                }
            }
        }
    }
}

GET_DATA_2 = {
    "title": "Get three different data sources",
    "description": "This process graph is the source for three different layer: raster, vector and strds",
    "process_graph": {
        "get_strds_data": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "CAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"
                }
            }
        },
        "get_lakes_data": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "nc_spm_08.PERMANENT.vector.lakes"
                }
            }
        },
        "get_elevation_data": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "nc_spm_08.PERMANENT.raster.elevation"
                }
            }
        }
    }
}

FILTER_BBOX = {
    "title": "Bounding box filtering of raster layer elevation",
    "description": "This process graph applies the bounding box filter to a raster layer",
    "process_graph": {
        "filter_bbox_1": {
            "process_id": "filter_bbox",
            "arguments": {
                "data": {"from_node": "get_data_1"},
                "left": -40.5,
                "right": 75.5,
                "top": 75.5,
                "bottom": 25.25,
                "width_res": 0.1,
                "height_res": 0.1,
            }
        },
        "get_data_1": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "nc_spm_08.PERMANENT.raster.elevation"
                }
            }
        }
    }
}

DATERANGE = {
    "title": "Filter the daterange of a single STRDS",
    "description": "Filter the daterange of a single STRDS",
    "process_graph": {
        "get_strds_data": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"
                }
            }
        },
        "filter_daterange_1": {
            "process_id": "filter_daterange",
            "arguments": {
                "data": {"from_node": "get_strds_data"},
                "from": "2001-01-01",
                "to": "2005-01-01",
            }
        }
    }
}

REDUCE_TIME_MIN = {
    "title": "Reduce the time dimension of a single STRDS",
    "description": "Reduce the time dimension of a single STRDS",
    "process_graph": {
        "get_strds_data": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"
                }
            }
        },
        "reduce_time_1": {
            "process_id": "reduce_time",
            "arguments": {
                "data": {"from_node": "get_strds_data"},
                "method": "minimum",
            }
        }
    }
}


NDVI_STRDS = {
    "title": "Compute the NDVI based on two STRDS",
    "description": "Compute the NDVI data from two space-time raster datasets",
    "process_graph": {
        "ndvi_1": {
            "process_id": "NDVI",
            "arguments": {
                "red": {"from_node": "get_red_data"},
                "nir": {"from_node": "get_nir_data"},
            }
        },
        "get_red_data": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "nc_spm_08.landsat.strds.lsat5_red"
                }
            }
        },
        "get_nir_data": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "nc_spm_08.landsat.strds.lsat5_nir"
                }
            }
        }
    }
}

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
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                }
            }
        }
    }
}

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
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
                }
            }
        }
    }
}


USE_CASE_1 = {
    "title": "Compute the NDVI based on two STRDS",
    "description": "Compute the NDVI data from two space-time raster datasets and apply several filters in the data",
    "process_graph": {
        "get_red_data": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "nc_spm_08.landsat.strds.lsat5_red"
                }
            }
        },
        "get_nir_data": {
            "process_id": "get_data",
            "arguments": {
                "data": {
                    "name": "nc_spm_08.landsat.strds.lsat5_nir"
                }
            }
        },
        "filter_bbox_red": {
            "process_id": "filter_bbox",
            "arguments": {
                "data": {"from_node": "get_red_data"},
                "left": -40.5,
                "right": 75.5,
                "top": 75.5,
                "bottom": 25.25,
                "width_res": 0.1,
                "height_res": 0.1,
            }
        },
        "filter_bbox_nir": {
            "process_id": "filter_bbox",
            "arguments": {
                "data": {"from_node": "get_nir_data"},
                "left": -40.5,
                "right": 75.5,
                "top": 75.5,
                "bottom": 25.25,
                "width_res": 0.1,
                "height_res": 0.1,
            }
        },
        "ndvi_1": {
            "process_id": "NDVI",
            "arguments": {
                "red": {"from_node": "filter_bbox_red"},
                "nir": {"from_node": "filter_bbox_nir"},
            }
        },
        "filter_daterange_ndvi": {
            "process_id": "filter_daterange",
            "arguments": {
                "data": {"from_node": "ndvi_1"},
                "from": "2001-01-01",
                "to": "2005-01-01",
            }
        },
        "reduce_time_1": {
            "process_id": "reduce_time",
            "arguments": {
                "data": {"from_node": "filter_daterange_ndvi"},
                "method": "minimum",
            }
        }
    }
}

OPENEO_EXAMPLE_1 = {
    "title": "NDVI based on Sentinel 2",
    "description": "Deriving minimum NDVI measurements over pixel time series of Sentinel 2",
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
                "from": "2017-01-01",
                "to": "2017-01-31"
            }
        },
        "filter2": {
            "process_id": "filter_temporal",
            "arguments": {
                "data": {
                    "from_node": "getcol1"
                },
                "from": "2018-01-01",
                "to": "2018-01-31"
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
            "process_id": "merge_collections",
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
            "process_id": "reduce",
            "arguments": {
                "data": {
                    "from_node": "mergec1"
                },
                "dimension": "temporal",
                "reducer": {
                    "callback": {
                        "min1": {
                            "process_id": "min",
                            "arguments": {
                                "data": {
                                    "from_argument": "dimension_data"
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
            "process_id": "reduce",
            "arguments": {
                "data": {
                    "from_node": "filter3"
                },
                "dimension": "spectral",
                "reducer": {
                    "callback": {
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
                            "process_id": "substract",
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
