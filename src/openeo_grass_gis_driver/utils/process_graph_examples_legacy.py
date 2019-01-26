# -*- coding: utf-8 -*-

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

get_data_1 = {
    "process_graph": {
        "process_id": "get_data",
        "data_id": "nc_spm_08.PERMANENT.raster.elevation"
    }
}

get_data_2 = {
    "process_graph": {
        "process_id": "get_data",
        "data_id": "nc_spm_08.PERMANENT.raster.elevation",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.PERMANENT.vector.lakes",
            "imagery": {
                "process_id": "get_data",
                "data_id": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"
            }
        }
    }
}

filter_bbox = {
    "process_graph": {
        "process_id": "filter_bbox",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.PERMANENT.raster.elevation"
        },
        "spatial_extent": {
            "left": -40.5,
            "right": 75.5,
            "top": 75.5,
            "bottom": 25.25,
            "width_res": 0.1,
            "height_res": 0.1,
        }
    }
}

daterange = {
    "process_graph": {
        "process_id": "filter_daterange",
        "from": "2001-01-01",
        "to": "2005-01-01",
        "strds_data": {
            "process_id": "get_data",
            "data_id": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"
        }

    }
}

reduce_time_min = {
    "process_graph": {
        "process_id": "reduce_time",
        "method": "minimum",
        "images": {
            "process_id": "get_data",
            "data_id": "ECAD.PERMANENT.strds.temperature_mean_1950_2013_yearly_celsius"
        }

    }
}

ndvi_1 = {
    "process_graph": {
        "process_id": "NDVI",
        "red": "lsat5_red",
        "nir": "lsat5_nir",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.landsat.strds.lsat5_red",
            "imagery": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.landsat.strds.lsat5_nir"
            }
        }
    }
}

ndvi_2 = {
    "process_graph": {
        "process_id": "NDVI",
        "red": "S2A_B04",
        "nir": "S2A_B08",
        "imagery": {
            "process_id": "get_data",
            "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08",
            "imagery": {
                "process_id": "get_data",
                "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
            }
        }
    }
}

ndvi_3 = {
    "process_graph": {
        "process_id": "NDVI2",
        "red": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.landsat.strds.lsat5_red"
        },
        "nir": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.landsat.strds.lsat5_nir"
        }
    }
}

ndvi_4 = {
    "process_graph": {
        "process_id": "NDVI2",
        "nir": {
            "process_id": "get_data",
            "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
        },
        "red": {
            "process_id": "get_data",
            "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
        }
    }
}

raster_export = {
    "process_graph": {
        "process_id": "raster_exporter",
        "imagery": {
            "process_id": "get_data",
            "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08",
            "imagery": {
                "process_id": "get_data",
                "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
            }
        }
    }
}

zonal_statistics = {
    "process_graph": {
        "process_id": "zonal_statistics",
        "imagery": {
            "process_id": "get_data",
            "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08",
            "imagery": {
                "process_id": "get_data",
                "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
            }
        },
        "polygons": "https://storage.googleapis.com/graas-geodata/roi_openeo_use_case_2.geojson"
    }
}

ndvi_error = {
    "process_graph": {
        "process_id": "NDVI_nope",
        "nir": {
            "process_id": "get_data",
            "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"
        },
        "red": {
            "process_id": "get_data",
            "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"
        }
    }
}

openeo_usecase_1 = {
    "process_graph": {
        "process_id": "reduce_time",
        "method": "minimum",
        "imagery": {
            "process_id": "NDVI2",
            "red": {
                "process_id": "filter_daterange",
                "from": "2001-01-01",
                "to": "2005-01-01",
                "imagery": {
                    "process_id": "filter_bbox",
                    "imagery": {
                        "process_id": "get_data",
                        "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04",
                    },
                    "spatial_extent": {
                        "left": -40.5,
                        "right": 75.5,
                        "top": 75.5,
                        "bottom": 25.25,
                        "width_res": 0.1,
                        "height_res": 0.1,
                    }
                }
            },
            "nir": {
                "process_id": "filter_daterange",
                "from": "2001-01-01",
                "to": "2005-01-01",
                "imagery": {
                    "process_id": "filter_bbox",
                    "imagery": {
                        "process_id": "get_data",
                        "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08",
                    },
                    "spatial_extent": {
                        "left": -40.5,
                        "right": 75.5,
                        "top": 75.5,
                        "bottom": 25.25,
                        "width_res": 0.1,
                        "height_res": 0.1,
                    }
                }
            }
        }

    }
}

openeo_usecase_1a = {
    "process_graph": {
        "process_id": "reduce_time",
        "method": "minimum",
        "imagery": {
            "process_id": "NDVI",
            "red": "S2A_B04",
            "nir": "S2A_B08",
            "imagery": {
                "process_id": "filter_daterange",
                "from": "2001-01-01",
                "to": "2005-01-01",
                "imagery": {
                    "process_id": "filter_bbox",
                    "imagery": {
                        "process_id": "get_data",
                        "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04",
                        "imagery": {
                            "process_id": "get_data",
                            "data_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08",
                        }
                    },
                    "spatial_extent": {
                        "left": -40.5,
                        "right": 75.5,
                        "top": 75.5,
                        "bottom": 25.25,
                        "width_res": 0.1,
                        "height_res": 0.1,
                    }
                }
            }

        }
    }
}

openeo_usecase_2 = \
    {
        "process_graph": {
            "process_id": "udf_reduce_time",
            "args": {
                "collections": [{
                    "process_id": "filter_daterange",
                    "args": {
                        "collections": [{
                            "process_id": "filter_bbox",
                            "args": {
                                "collections": [{"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B04"},
                                                {"product_id": "LL.sentinel2A_openeo_subset.strds.S2A_B08"}],
                                "left": -5.0,
                                "right": -4.7,
                                "top": 39.3,
                                "bottom": 39.0,
                                "ewres": 0.1,
                                "nsres": 0.1,
                                "srs": "EPSG:4326"
                            }
                        }],
                        "from": "1980-01-01 00:00:00",
                        "to": "2010-01-01 00:00:00"
                    }
                }],
                "python_file_url": "https://storage.googleapis.com/datentransfer/aggr_func.py"
            }
        }
    }
