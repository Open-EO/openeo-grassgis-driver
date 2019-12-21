# -*- coding: utf-8 -*-

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"

GET_DATA_1 = {
    "process_graph": {
        "process_id": "get_data",
        "data_id": "nc_spm_08.PERMANENT.raster.elevation"
    }
}

GET_DATA_2 = {
    "process_graph": {
        "process_id": "get_data",
        "data_id": "nc_spm_08.PERMANENT.raster.elevation",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.PERMANENT.vector.lakes",
        }
    }
}

GET_DATA_3 = {
    "process_graph": {
        "process_id": "get_data",
        "data_id": "latlong_wgs84.asia_gdd_2017.strds.gdd"
    }
}

FILTER_BOX = {
    "process_graph": {
        "process_id": "filter_bbox",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.PERMANENT.raster.elevation"
        },
        "extent": {
            "west": 630000,
            "east": 645000,
            "north": 228500,
            "south": 215000,
            "crs": "+proj=lcc +lat_1=36.16666666666666 +lat_2=34.33333333333334 +lat_0=33.75 +lon_0=-79 +x_0=609601.22 +y_0=0 +no_defs +a=6378137 +rf=298.257222101 +towgs84=0.000,0.000,0.000 +to_meter=1",
        }
    }
}

DATERANGE = {
    "process_graph": {
        "process_id": "filter_daterange",
        "from": "2001-01-01",
        "to": "2005-01-01",
        "strds_data": {
            "process_id": "get_data",
            "data_id": "latlong_wgs84.modis_ndvi_global.strds.ndvi_16_5600m"
        }

    }
}

REDUCE_TIME_MIN = {
    "process_graph": {
        "process_id": "reduce_time",
        "method": "minimum",
        "images": {
            "process_id": "get_data",
            "data_id": "latlong_wgs84.modis_ndvi_global.strds.ndvi_16_5600m"
        }

    }
}

NDVI_1 = {
    "process_graph": {
        "process_id": "ndvi",
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

NDVI_2 = {
    "process_graph": {
        "process_id": "ndvi",
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

NDVI_3 = {
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

NDVI_4 = {
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

RASTER_EXPORT = {
    "process_graph": {
        "process_id": "raster_exporter",
        "imagery": {
            "process_id": "get_data",
            "data_id": "nc_spm_08.PERMANENT.raster.elevation",
            "imagery": {
                "process_id": "get_data",
                "data_id": "nc_spm_08.PERMANENT.raster.slope"
            }
        }
    }
}

ZONAL_STATISTICS_SINGLE = {
    "process_graph": {
        "process_id": "zonal_statistics",
        "imagery": {
            "process_id": "get_data",
            "data_id": "latlong_wgs84.modis_ndvi_global.strds.ndvi_16_5600m",
        },
        "polygons": "https://storage.googleapis.com/graas-geodata/roi_openeo_use_case_2.geojson"
    }
}

ZONAL_STATISTICS = {
    "process_graph": {
        "process_id": "zonal_statistics",
        "imagery": {
            "process_id": "get_data",
            "data_id": "latlong_wgs84.modis_ndvi_global.strds.ndvi_16_5600m",
            "imagery": {
                "process_id": "get_data",
                "data_id": "latlong_wgs84.asia_gdd_2017.strds.gdd"
            }
        },
        "polygons": "https://storage.googleapis.com/graas-geodata/roi_openeo_use_case_2.geojson"
    }
}

NDVI_ERROR = {
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

OPENEO_USECASE_1 = {
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
                    "extent": {
                        "west": -40.5,
                        "east": 75.5,
                        "north": 75.5,
                        "south": 25.25,
                        "crs": "+proj=longlat +no_defs +a=6378137 +rf=298.257223563 +towgs84=0.000,0.000,0.000",
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
                    "extent": {
                        "west": -40.5,
                        "east": 75.5,
                        "north": 75.5,
                        "south": 25.25,
                        "crs": "+proj=longlat +no_defs +a=6378137 +rf=298.257223563 +towgs84=0.000,0.000,0.000",
                    }
                }
            }
        }

    }
}

OPENEO_USECASE_1A = {
    "process_graph": {
        "process_id": "reduce_time",
        "method": "minimum",
        "imagery": {
            "process_id": "ndvi",
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
                    "extent": {
                        "west": -40.5,
                        "east": 75.5,
                        "north": 75.5,
                        "south": 25.25,
                        "crs": "+proj=longlat +no_defs +a=6378137 +rf=298.257223563 +towgs84=0.000,0.000,0.000",
                    }
                }
            }

        }
    }
}

OPENEO_USECASE_2 = \
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
                                "west": -5.0,
                                "east": -4.7,
                                "north": 39.3,
                                "south": 39.0,
                                "crs": "EPSG:4326"
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
