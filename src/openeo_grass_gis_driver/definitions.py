# -*- coding: utf-8 -*-
from flask_restful_swagger_2 import Schema

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessDescription(Schema):
    description = "Defines and describes a process including its expected input arguments."
    type = "object"
    required = ["process_id", "description"]
    properties = {
        "process_id": {
            "type": "string",
            "description": "The unique identifier of the process."
        },
        "description": {
            "type": "string",
            "description": "A short and concise description of what the process does and how the output looks like."
        },
        "link": {
            "type": "string",
            "description": "Reference to an external process definition if the process has been defined "
                           "over different back ends within OpenEO"
        },
        "args": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "required": ["description"],
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "A short and concise description of the process argument."
                    },
                    "required": {
                        "type": "boolean",
                        "default": True,
                        "description": "Defines whether an argument is required or optional."
                    }
                },
                "additionalProperties": True,
                "description": "**DEFAULT VALUES FOR ARGUMENTS ARE NOT FORMALIZED IN THE SWAGGER 2.0 "
                               "DEFINITION DUE TO MISSING SUPPORT FOR oneOf OR anyOf SCHEMA COMBINATIONS.**"
            }
        }
    }
    example = {
        "process_id": "band_arithmetic",
        "description": "Perform basic arithmetic expressions on individual pixel and their band values.",
        "args": {
            "imagery": {
                "description": "input image or image collection",
                "required": True
            },
            "expr": {
                "description": "expressions as array, the result will have as many bands as the number "
                               "of given expressions."
            }
        }
    }


#####################################################################

class ProcessListEntry(Schema):
    type = "object"
    description = "A single entry of the process description list"
    required = ["process_id", "description"]
    properties = {
        "process_id": {"type": "string"},
        "description": {"type": "string"}
    }
    example = {
        "process_id": "NDVI",
        "description": "Computes the normalized difference vegetation index (NDVI) for "
                       "all pixels of the input dataset."
    }
    additionalProperties = True


#####################################################################

class SpatialExtent(Schema):
    type = "object"
    description = "spatial extent of the available imagery"
    properties = {
        "crs": {
            "description": "Coordinate reference system. EPSG codes must be supported. "
                           "In addition, proj4 strings should be supported by back-ends. "
                           "Whenever possible, it is recommended to use EPSG codes instead "
                           "of proj4 strings. Defaults to EPSG:4326 unless the client explicitly "
                           "requests a different coordinate reference system. Reference systems "
                           "MUST be accepted case insensitive.",
            "type": "string",
            "default": "EPSG:4326"
        },
        "left": {"type": "number"},
        "right": {"type": "number"},
        "top": {"type": "number"},
        "bottom": {"type": "number"}
    }


#####################################################################

class BandDataTypes(Schema):
    type = "string"
    description = "Data type for band values including its bit size."
    enum = ["uint8", "uint16", "uint32", "uint64", "int8", "int16", "int32",
            "int64", "float16", "float32", "float64"]


#####################################################################

class BandDescription(Schema):
    type = "object"
    required = ["band_id"]
    additionalProperties = True
    properties = {
        "band_id": {
            "description": "unique identifier for bands",
            "type": "string"
        },
        "name": {
            "description": "optional name to refer to bands by name such as 'red' instead of their band_id.",
            "type": "string"
        },
        "type": BandDataTypes,
        "offset": {
            "description": "offset to convert band values to the actual measurement scale.",
            "type": "number",
            "default": 0
        },
        "scale": {
            "description": "scale to convert band values to the actual measurement scale.",
            "type": "number",
            "default": 1
        },
        "unit": {
            "description": "unit of measurements (preferably SI)",
            "type": "string"
        },
        "nodata": {
            "description": "specific values representing no data",
            "type": "array",
            "items": {"type": "number"}
        },
        "wavelength_nm": {
            "description": "Wavelength of the band in nanometers.",
            "type": "number",
        },
        "res_m": {
            "description": "Spatial resolution of the band in meters.",
            "type": "number",
        }
    }


#####################################################################

class DataSetListEntry(Schema):
    type = "object"
    properties = {
        "data_id": {"type": "string"},
        "description": {"type": "string"},
        "source": {"type": "string"}
    }
    additionalProperties = True


#####################################################################

class DataSetInfo(Schema):
    type = "object"
    required = ["product_id", "description", "extent", "bands"]
    properties = {
        "product_id": {"type": "string"},
        "description": {"type": "string"},
        "source": {"type": "string"},
        "extent": SpatialExtent,
        "time": {"description": "Temporal extent specified by a start and an end time, each formatted as "
                                "a RFC 3339 date-time. Open date ranges are supported and can be specified "
                                "by setting one of the times to null. Setting both entries to null is not allowed.",
                 "type": "array",
                 "items": {"type": "string"}
                 },
        "bands": {"type": "array", "items": BandDataTypes}
    }
    additionalProperties = True


#####################################################################

class UDFTypen(Schema):
    type = "string"
    description = "The UDF types define how UDFs can be exposed to the data, how they can be parallelized, " \
                  "and how the result schema should be structured."
    enum = ["apply_pixel", "apply_scene", "reduce_time", "reduce_space", "window_time", "window_space",
            "window_spacetime", "agregate_time", "aggregate_space", "aggregate_spacetime"]


#####################################################################

class UDFDescription(Schema):
    description = "Defines and describes a UDF using the same schema as the description of " \
                  "processes offered by the back-end."
    type = "object"
    required = ["process_id", "description"]
    properties = {
        "process_id": {
            "type": "string",
            "description": "The unique identifier of the process."
        },
        "description": {
            "type": "string",
            "description": "A short and concise description of what the process does and how the output looks like."
        },
        "link": {
            "type": "string",
            "description": "Reference to an external process definition if the process has been "
                           "defined over different back-ends within OpenEO"
        },
        "args": {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "required": ["description"],
                "properties": {
                    "description": {
                        "type": "string",
                        "description": "A short and concise description of the process argument."
                    },
                    "required": {
                        "type": "boolean",
                        "default": True,
                        "description": "Defines whether an argument is required or optional."
                    }
                },
                "additionalProperties": True,
                "description": "**DEFAULT VALUES FOR ARGUMENTS ARE NOT FORMALIZED IN THE SWAGGER 2.0 "
                               "DEFINITION DUE TO MISSING SUPPORT FOR oneOf OR anyOf SCHEMA COMBINATIONS.**"
            }
        }
    }
    example = {
        "process_id": "udf/R/reduce_time",
        "description": "Applies an R function independently over all input time series that produces a "
                       "zero-dimensional value (scalar or multi-band tuple) as output (per time series).",
        "args": {
            "imagery": {
                "description": "input (image) time series",
                "required": True
            },
            "script": {
                "description": "Script resource that has been uploaded to user space before. ",
                "required": True
            }
        }
    }


#####################################################################

class UserId(Schema):
    description = "User id"
    type = "string"
    additionalProperties = True


#####################################################################

class FileDescription(Schema):
    description = "File description of user specific files"
    type = "object"
    required = ["name", "size", "modified"]
    additionalProperties = True
    properties = {
        "name": {
            "type": "string",
            "description": "The name of the file."
        },
        "size": {
            "type": "integer",
            "description": "The size of the file in bytes."
        },
        "modified": {
            "type": "string",
            "description": "The creation/modification time of the file."
        }
    }
    example = {
        "name": "test.txt",
        "size": 182,
        "modified": "2015-10-20T17:22:10Z"
    }


#####################################################################

class ArgSet(Schema):
    description = "Defines an object schema for collection (uniquely named) arguments as input to processes. " \
                  "**THIS TYPE IS NOT FORMALIZED IN THE SWAGGER 2.0 DEFINITION DUE TO MISSING SUPPORT FOR oneOf " \
                  "OR anyOf SCHEMA COMBINATIONS.**"
    type = "object"
    additionalProperties = True


#####################################################################

class ProcessGraph(Schema):
    description = "A process graph defines an executable process, i.e. one process or a combination of chained " \
                  "processes including specific arguments."
    type = "object"
    required = ["process_id"]
    properties = {
        "process_id": {
            "type": "string",
            "description": "The unique identifier of the process."
        },
        "args": {
            "type": "array",
            "items": ArgSet,
            "description": "Collection of arguments identified by their name."
        }
    }
    example = {
        "process_id": "median_time",
        "args": {
            "imagery": {
                "process_id": "NDVI",
                "args": {
                    "imagery": {
                        "process_id": "filter_daterange",
                        "args": {"imagery": {"product_id": "Sentinel2A-L1C"}},
                        "from": "2017-01-01",
                        "to": "2017-01-31"
                    }
                },
                "red": "4",
                "nir": "8"
            }
        }
    }


#####################################################################

class View(Schema):
    description = "The view defines how we look at the data (spatial extent, resolution, time range, etc.) for " \
                  "processing. It can be used to experiment with tasks and processes on small subdataset."
    type = "object"
    additionalProperties = True
    properties = {
        "space": {
            "description": "Defines spatial resolution, window, and resampling method used for running "
                           "processes on small sub datasets",
            "type": "object",
            "properties": {
                "srs": {
                    "type": "string",
                    "description": "Spatial reference system as proj4 string or EPSG code such as `EPSG:3857`"
                },
                "window": {
                    "type": "object",
                    "description": "boundaries of the spatial window as coordinates expressed in the "
                                   "given reference system.",
                    "required": ["left", "top", "right", "bottom"],
                    "properties": {
                        "left": {"type": "number"},
                        "top": {"type": "number"},
                        "right": {"type": "number"},
                        "bottom": {"type": "number"}
                    }
                },
                "cell_size": {"type": "number"},
                "resampling": {
                    "type": "string",
                    "description": "resampling method to use (taken from [GDAL]"
                                   "(https://www.gdal.org/gdal_translate.html))",
                    "default": "nearest",
                    "enum": ["nearest", "bilinear", "cubic", "cubicspline", "lanczos", "average", "mode"]
                }
            },
            "example": {
                "srs": "EPSG:4326",
                "window": {
                    "left": -10.21,
                    "top": 53.23,
                    "right": 12.542,
                    "bottom": 12.32
                },
                "resolution": 0.25,
                "resampling": "nearest"
            }
        },
        "time": {
            "description": "Defines temporal resolution, window, and resampling method used for running processes "
                           "on small sub datasets",
            "type": "object",
            "properties": {
                "window": {
                    "type": "object",
                    "description": "Start and end date/time in ISO 8601 format",
                    "required": [
                        "start",
                        "end"
                    ],
                    "properties": {
                        "start": {
                            "type": "string",
                            "format": "dateTime"
                        },
                        "end": {
                            "type": "string",
                            "format": "dateTime"
                        }
                    }
                },
                "time_step": {
                    "type": "string",
                    "description": "temporal granularity given as ISO 8601 time duration. In order to avoid mixing "
                                   "inconsistent durations such as `P1M30DT24H` only a single integer number with "
                                   "date/time component such as `P1M`, `P30D`, `PT24H` should be specified."
                },
                "resampling": {
                    "type": "string",
                    "description": "resampling method to use "
                                   "(taken from [GDAL](https://www.gdal.org/gdal_translate.html))",
                    "default": "nearest",
                    "enum": [
                        "nearest",
                        "bilinear",
                        "cubic",
                        "cubicspline",
                        "lanczos",
                        "average",
                        "mode"
                    ]
                }
            },
            "example": {
                "window": {
                    "start": "2017-01-01",
                    "end": "2018-01-01"
                },
                "resolution": "P1M",
                "resampling": "nearest"
            }
        }
    }


#####################################################################

class Job(Schema):
    description = "Defines metadata of processing jobs that have been submitted by users."
    type = "object"
    required = ["job_id", "status", "process_graph", "user_id"]
    additionalProperties = True
    properties = {
        "job_id": {
            "type": "string",
            "description": "Unique identifier of a job that is generated by the back-end during job submission."
        },
        "status": {
            "type": "string",
            "enum": ["submitted", "running", "finished", "canceled", "error", "unknown", "waiting"],
            "description": "The current status of the job."
        },
        "process_graph": ProcessGraph,
        "view": View,
        "submitted": {
            "type": "string",
            "format": "dateTime",
            "description": "Date and time of job submission in ISO 8601 format"
        },
        "last_update": {
            "type": "string",
            "format": "dateTime",
            "description": "Date and time of last status change in ISO 8601 format"
        },
        "user_id": {
            "type": "string",
            "description": "Identifier of the user, who submitted the job and pays incurred costs if needed."
        },
        "consumed_credits": {
            "type": "number",
            "description": "Credits consumed by this process"
        }
    }
    example = {
        "job_id": "748df7caa8c84a7ff6e",
        "user_id": "bd6f9faf93b4",
        "status": "running",
        "process_graph": {
            "process_id": "filter_daterange",
            "args": [
                {"A": {"product_id": "Sentinel2A-L1C"}},
                {"from": "2017-01-01"},
                {"to": "2017-01-31"}
            ]
        },
        "submitted": "2017-01-01T09:32:12Z",
        "last_update": "2017-01-01T09:36:18Z",
        "consumed_credits": "392"
    }
