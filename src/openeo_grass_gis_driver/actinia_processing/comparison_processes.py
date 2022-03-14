# -*- coding: utf-8 -*-
import json

from openeo_grass_gis_driver.actinia_processing.base import \
     check_node_parents, DataObject, GrassDataType, \
     create_output_name
from openeo_grass_gis_driver.models.process_graph_schemas import \
     ProcessGraphNode, ProcessGraph
from openeo_grass_gis_driver.models.process_schemas import \
     Parameter, ProcessDescription, ReturnValue, ProcessExample
from .base import PROCESS_DICT, PROCESS_DESCRIPTION_DICT, Node

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2022, Markus Metz, mundialis"
__maintainer__ = "Markus Metz"
__email__ = "metz@mundialis.de"

# dummy comparison processes
# these processes do not take a datacube as input, but one or more numbers


PROCESS_DESCRIPTION_DICT["array_contains"] = {
  "id": "array_contains",
  "summary": "Check whether the array contains a given value",
  "description": "Checks whether the array specified for `data` contains the value specified in `value`. Returns `true` if there's a match, otherwise `false`.\n\n**Remarks:**\n\n* To get the index or the label of the value found, use ``array_find()``.\n* All definitions for the process ``eq()`` regarding the comparison of values apply here as well. A `null` return value from ``eq()`` is handled exactly as `false` (no match).\n* Data types MUST be checked strictly. For example, a string with the content *1* is not equal to the number *1*.\n* An integer *1* is equal to a floating-point number *1.0* as `integer` is a sub-type of `number`. Still, this process may return unexpectedly `false` when comparing floating-point numbers due to floating-point inaccuracy in machine-based computation.\n* Temporal strings are treated as normal strings and MUST NOT be interpreted.\n* If the specified value is an array, object or null, the process always returns `false`. See the examples for one to check for `null` values.",
  "categories": [
    "arrays",
    "comparison",
    "reducer"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "List to find the value in.",
      "schema": {
        "type": "array",
        "items": {
          "description": "Any data type is allowed."
        }
      }
    },
    {
      "name": "value",
      "description": "Value to find in `data`.",
      "schema": {
        "description": "Any data type is allowed."
      }
    }
  ],
  "returns": {
    "description": "`true` if the list contains the value, false` otherwise.",
    "schema": {
      "type": "boolean"
    }
  },
  "examples": [
    {
      "arguments": {
        "data": [
          1,
          2,
          3
        ],
        "value": 2
      },
      "returns": true
    },
    {
      "arguments": {
        "data": [
          "A",
          "B",
          "C"
        ],
        "value": "b"
      },
      "returns": false
    },
    {
      "arguments": {
        "data": [
          1,
          2,
          3
        ],
        "value": "2"
      },
      "returns": false
    },
    {
      "arguments": {
        "data": [
          1,
          2,
          null
        ],
        "value": null
      },
      "returns": true
    },
    {
      "arguments": {
        "data": [
          [
            1,
            2
          ],
          [
            3,
            4
          ]
        ],
        "value": [
          1,
          2
        ]
      },
      "returns": false
    },
    {
      "arguments": {
        "data": [
          [
            1,
            2
          ],
          [
            3,
            4
          ]
        ],
        "value": 2
      },
      "returns": false
    },
    {
      "arguments": {
        "data": [
          {
            "a": "b"
          },
          {
            "c": "d"
          }
        ],
        "value": {
          "a": "b"
        }
      },
      "returns": false
    }
  ],
  "links": [
    {
      "rel": "example",
      "type": "application/json",
      "href": "https://processes.openeo.org/1.2.0/examples/array_contains_nodata.json",
      "title": "Check for no-data values in arrays"
    }
  ],
  "process_graph": {
    "find": {
      "process_id": "array_find",
      "arguments": {
        "data": {
          "from_parameter": "data"
        },
        "value": {
          "from_parameter": "value"
        }
      }
    },
    "is_nodata": {
      "process_id": "is_nodata",
      "arguments": {
        "x": {
          "from_node": "find"
        }
      }
    },
    "not": {
      "process_id": "not",
      "arguments": {
        "x": {
          "from_node": "is_nodata"
        }
      },
      "result": true
    }
  }
}


PROCESS_DESCRIPTION_DICT["between"] = {
  "id": "between",
  "summary": "Between comparison",
  "description": "By default, this process checks whether `x` is greater than or equal to `min` and lower than or equal to `max`, which is the same as computing `and(gte(x, min), lte(x, max))`. Therefore, all definitions from ``and()``, ``gte()`` and ``lte()`` apply here as well.\n\nIf `exclude_max` is set to `true` the upper bound is excluded so that the process checks whether `x` is greater than or equal to `min` and lower than `max`. In this case, the process works the same as computing `and(gte(x, min), lt(x, max))`.\n\nLower and upper bounds are not allowed to be swapped. So `min` MUST be lower than or equal to `max` or otherwise the process always returns `false`.",
  "categories": [
    "comparison"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "The value to check.",
      "schema": {
        "description": "Any data type is allowed."
      }
    },
    {
      "name": "min",
      "description": "Lower boundary (inclusive) to check against.",
      "schema": [
        {
          "type": "number"
        },
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
          "format": "time",
          "subtype": "time"
        }
      ]
    },
    {
      "name": "max",
      "description": "Upper boundary (inclusive) to check against.",
      "schema": [
        {
          "type": "number"
        },
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
          "format": "time",
          "subtype": "time"
        }
      ]
    },
    {
      "name": "exclude_max",
      "description": "Exclude the upper boundary `max` if set to `true`. Defaults to `false`.",
      "schema": {
        "type": "boolean"
      },
      "default": false,
      "optional": true
    }
  ],
  "returns": {
    "description": "`true` if `x` is between the specified bounds, otherwise `false`.",
    "schema": {
      "type": [
        "boolean",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": null,
        "min": 0,
        "max": 1
      },
      "returns": null
    },
    {
      "arguments": {
        "x": 1,
        "min": 0,
        "max": 1
      },
      "returns": true
    },
    {
      "arguments": {
        "x": 1,
        "min": 0,
        "max": 1,
        "exclude_max": true
      },
      "returns": false
    },
    {
      "description": "Swapped bounds (min is greater than max) MUST always return `false`.",
      "arguments": {
        "x": 0.5,
        "min": 1,
        "max": 0
      },
      "returns": false
    },
    {
      "arguments": {
        "x": -0.5,
        "min": -1,
        "max": 0
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "00:59:59Z",
        "min": "01:00:00+01:00",
        "max": "01:00:00Z"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "2018-07-23T17:22:45Z",
        "min": "2018-01-01T00:00:00Z",
        "max": "2018-12-31T23:59:59Z"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "2000-01-01",
        "min": "2018-01-01",
        "max": "2020-01-01"
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "2018-12-31T17:22:45Z",
        "min": "2018-01-01",
        "max": "2018-12-31"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "2018-12-31T17:22:45Z",
        "min": "2018-01-01",
        "max": "2018-12-31",
        "exclude_max": true
      },
      "returns": false
    }
  ],
  "process_graph": {
    "gte": {
      "process_id": "gte",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": {
          "from_parameter": "min"
        }
      }
    },
    "lte": {
      "process_id": "lte",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": {
          "from_parameter": "max"
        }
      }
    },
    "lt": {
      "process_id": "lt",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": {
          "from_parameter": "max"
        }
      }
    },
    "if": {
      "process_id": "if",
      "arguments": {
        "value": {
          "from_parameter": "exclude_max"
        },
        "accept": {
          "from_node": "lte"
        },
        "reject": {
          "from_node": "lt"
        }
      }
    },
    "and": {
      "process_id": "and",
      "arguments": {
        "x": {
          "from_node": "gte"
        },
        "y": {
          "from_node": "if"
        }
      },
      "result": true
    }
  }
}


PROCESS_DESCRIPTION_DICT["eq"] = {
  "id": "eq",
  "summary": "Equal to comparison",
  "description": "Compares whether `x` is strictly equal to `y`.\n\n**Remarks:**\n\n* Data types MUST be checked strictly. For example, a string with the content *1* is not equal to the number *1*. Nevertheless, an integer *1* is equal to a floating-point number *1.0* as `integer` is a sub-type of `number`.\n* If any operand is `null`, the return value is `null`. Therefore, `eq(null, null)` returns `null` instead of `true`.\n* If any operand is an array or object, the return value is `false`.\n* Strings are expected to be encoded in UTF-8 by default.\n* Temporal strings MUST be compared differently than other strings and MUST NOT be compared based on their string representation due to different possible representations. For example, the time zone representation `Z` (for UTC) has the same meaning as `+00:00`.",
  "categories": [
    "texts",
    "comparison"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "First operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    },
    {
      "name": "y",
      "description": "Second operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    },
    {
      "name": "delta",
      "description": "Only applicable for comparing two numbers. If this optional parameter is set to a positive non-zero number the equality of two numbers is checked against a delta value. This is especially useful to circumvent problems with floating-point inaccuracy in machine-based computation.\n\nThis option is basically an alias for the following computation: `lte(abs(minus([x, y]), delta)`",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      },
      "default": null,
      "optional": true
    },
    {
      "name": "case_sensitive",
      "description": "Only applicable for comparing two strings. Case sensitive comparison can be disabled by setting this parameter to `false`.",
      "schema": {
        "type": "boolean"
      },
      "default": true,
      "optional": true
    }
  ],
  "returns": {
    "description": "`true` if `x` is equal to `y`, `null` if any operand is `null`, otherwise `false`.",
    "schema": {
      "type": [
        "boolean",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 1,
        "y": null
      },
      "returns": null
    },
    {
      "arguments": {
        "x": null,
        "y": null
      },
      "returns": null
    },
    {
      "arguments": {
        "x": 1,
        "y": 1
      },
      "returns": true
    },
    {
      "arguments": {
        "x": 1,
        "y": "1"
      },
      "returns": false
    },
    {
      "arguments": {
        "x": 0,
        "y": false
      },
      "returns": false
    },
    {
      "arguments": {
        "x": 1.02,
        "y": 1,
        "delta": 0.01
      },
      "returns": false
    },
    {
      "arguments": {
        "x": -1,
        "y": -1.001,
        "delta": 0.01
      },
      "returns": true
    },
    {
      "arguments": {
        "x": 115,
        "y": 110,
        "delta": 10
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "Test",
        "y": "test"
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "Test",
        "y": "test",
        "case_sensitive": false
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "Ä",
        "y": "ä",
        "case_sensitive": false
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "00:00:00+00:00",
        "y": "00:00:00Z"
      },
      "returns": true
    },
    {
      "description": "`y` is not a valid date-time representation and therefore will be treated as a string so that the provided values are not equal.",
      "arguments": {
        "x": "2018-01-01T12:00:00Z",
        "y": "2018-01-01T12:00:00"
      },
      "returns": false
    },
    {
      "description": "01:00 in the time zone +1 is equal to 00:00 in UTC.",
      "arguments": {
        "x": "2018-01-01T00:00:00Z",
        "y": "2018-01-01T01:00:00+01:00"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": [
          1,
          2,
          3
        ],
        "y": [
          1,
          2,
          3
        ]
      },
      "returns": false
    }
  ]
}


PROCESS_DESCRIPTION_DICT["gt"] = {
  "id": "gt",
  "summary": "Greater than comparison",
  "description": "Compares whether `x` is strictly greater than `y`.\n\n**Remarks:**\n\n* If any operand is `null`, the return value is `null`.\n* If any operand is an array or object, the return value is `false`.\n* If any operand is not a `number` or temporal string (`date`, `time` or `date-time`), the process returns `false`.\n* Temporal strings can *not* be compared based on their string representation due to the time zone / time-offset representations.",
  "categories": [
    "comparison"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "First operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    },
    {
      "name": "y",
      "description": "Second operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    }
  ],
  "returns": {
    "description": "`true` if `x` is strictly greater than `y` or `null` if any operand is `null`, otherwise `false`.",
    "schema": {
      "type": [
        "boolean",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 1,
        "y": null
      },
      "returns": null
    },
    {
      "arguments": {
        "x": 0,
        "y": 0
      },
      "returns": false
    },
    {
      "arguments": {
        "x": 2,
        "y": 1
      },
      "returns": true
    },
    {
      "arguments": {
        "x": -0.5,
        "y": -0.6
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "00:00:00Z",
        "y": "00:00:00+01:00"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "1950-01-01T00:00:00Z",
        "y": "2018-01-01T12:00:00Z"
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "2018-01-01T12:00:00+00:00",
        "y": "2018-01-01T12:00:00Z"
      },
      "returns": false
    },
    {
      "arguments": {
        "x": true,
        "y": 0
      },
      "returns": false
    },
    {
      "arguments": {
        "x": true,
        "y": false
      },
      "returns": false
    }
  ]
}


PROCESS_DESCRIPTION_DICT["gte"] = {
  "id": "gte",
  "summary": "Greater than or equal to comparison",
  "description": "Compares whether `x` is greater than or equal to `y`.\n\n**Remarks:**\n\n* If any operand is `null`, the return value is `null`. Therefore, `gte(null, null)` returns `null` instead of `true`.\n* If any operand is an array or object, the return value is `false`.\n* If the operands are not equal (see process ``eq()``) and any of them is not a `number` or temporal string (`date`, `time` or `date-time`), the process returns `false`.\n* Temporal strings can *not* be compared based on their string representation due to the time zone / time-offset representations.",
  "categories": [
    "comparison"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "First operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    },
    {
      "name": "y",
      "description": "Second operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    }
  ],
  "returns": {
    "description": "`true` if `x` is greater than or equal to `y`, `null` if any operand is `null`, otherwise `false`.",
    "schema": {
      "type": [
        "boolean",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 1,
        "y": null
      },
      "returns": null
    },
    {
      "arguments": {
        "x": 0,
        "y": 0
      },
      "returns": true
    },
    {
      "arguments": {
        "x": 1,
        "y": 2
      },
      "returns": false
    },
    {
      "arguments": {
        "x": -0.5,
        "y": -0.6
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "00:00:00Z",
        "y": "00:00:00+01:00"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "1950-01-01T00:00:00Z",
        "y": "2018-01-01T12:00:00Z"
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "2018-01-01T12:00:00+00:00",
        "y": "2018-01-01T12:00:00Z"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": true,
        "y": false
      },
      "returns": false
    },
    {
      "arguments": {
        "x": [
          1,
          2,
          3
        ],
        "y": [
          1,
          2,
          3
        ]
      },
      "returns": false
    }
  ],
  "process_graph": {
    "eq": {
      "process_id": "eq",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": {
          "from_parameter": "y"
        }
      }
    },
    "gt": {
      "process_id": "gt",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": {
          "from_parameter": "y"
        }
      }
    },
    "or": {
      "process_id": "or",
      "arguments": {
        "x": {
          "from_node": "gt"
        },
        "y": {
          "from_node": "eq"
        }
      },
      "result": true
    }
  }
}


PROCESS_DESCRIPTION_DICT["if"] = {
  "id": "if",
  "summary": "If-Then-Else conditional",
  "description": "If the value passed is `true`, returns the value of the `accept` parameter, otherwise returns the value of the `reject` parameter.\n\nThis is basically an if-then-else construct as in other programming languages.",
  "categories": [
    "logic",
    "comparison",
    "masks"
  ],
  "parameters": [
    {
      "name": "value",
      "description": "A boolean value.",
      "schema": {
        "type": [
          "boolean",
          "null"
        ]
      }
    },
    {
      "name": "accept",
      "description": "A value that is returned if the boolean value is `true`.",
      "schema": {
        "description": "Any data type is allowed."
      }
    },
    {
      "name": "reject",
      "description": "A value that is returned if the boolean value is **not** `true`. Defaults to `null`.",
      "schema": {
        "description": "Any data type is allowed."
      },
      "default": null,
      "optional": true
    }
  ],
  "returns": {
    "description": "Either the `accept` or `reject` argument depending on the given boolean value.",
    "schema": {
      "description": "Any data type is allowed."
    }
  },
  "examples": [
    {
      "arguments": {
        "value": true,
        "accept": "A",
        "reject": "B"
      },
      "returns": "A"
    },
    {
      "arguments": {
        "value": null,
        "accept": "A",
        "reject": "B"
      },
      "returns": "B"
    },
    {
      "arguments": {
        "value": false,
        "accept": [
          1,
          2,
          3
        ],
        "reject": [
          4,
          5,
          6
        ]
      },
      "returns": [
        4,
        5,
        6
      ]
    },
    {
      "arguments": {
        "value": true,
        "accept": 123
      },
      "returns": 123
    },
    {
      "arguments": {
        "value": false,
        "accept": 1
      },
      "returns": null
    }
  ]
}


PROCESS_DESCRIPTION_DICT["is_nan"] = {
  "id": "is_nan",
  "summary": "Value is not a number",
  "description": "Checks whether the specified value `x` is not a number. Returns `true` for numeric values (integers and floating-point numbers), except for the special value `NaN` as defined by the [IEEE Standard 754](https://ieeexplore.ieee.org/document/4610935). All non-numeric data types MUST also return `true`, including arrays that contain `NaN` values.",
  "categories": [
    "comparison",
    "math > constants"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "The data to check.",
      "schema": {
        "description": "Any data type is allowed."
      }
    }
  ],
  "returns": {
    "description": "`true` if the data is not a number, otherwise `false`.",
    "schema": {
      "type": "boolean"
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 1
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "Test"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": null
      },
      "returns": true
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/4610935",
      "title": "IEEE Standard 754-2008 for Floating-Point Arithmetic"
    },
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/NaN.html",
      "title": "NaN explained by Wolfram MathWorld"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["is_nodata"] = {
  "id": "is_nodata",
  "summary": "Value is a no-data value",
  "description": "Checks whether the specified data is missing data, i.e. equals to `null` or any of the no-data values specified in the metadata. The special numerical value `NaN` (not a number) as defined by the [IEEE Standard 754](https://ieeexplore.ieee.org/document/4610935) is not considered no-data and must return `false`.",
  "categories": [
    "comparison"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "The data to check.",
      "schema": {
        "description": "Any data type is allowed."
      }
    }
  ],
  "returns": {
    "description": "`true` if the data is a no-data value, otherwise `false`.",
    "schema": {
      "type": "boolean"
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 1
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "Test"
      },
      "returns": false
    },
    {
      "arguments": {
        "x": null
      },
      "returns": true
    },
    {
      "arguments": {
        "x": [
          null,
          null
        ]
      },
      "returns": false
    }
  ]
}


PROCESS_DESCRIPTION_DICT["is_valid"] = {
  "id": "is_valid",
  "summary": "Value is valid data",
  "description": "Checks whether the specified value `x` is valid. The following values are considered valid:\n\n* Any finite numerical value (integers and floating-point numbers). The definition of finite numbers follows the [IEEE Standard 754](https://ieeexplore.ieee.org/document/4610935) and excludes the special value `NaN` (not a number).\n* Any other value that is not a no-data value according to ``is_nodata()`. Thus all arrays, objects and strings are valid, regardless of their content.",
  "categories": [
    "comparison"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "The data to check.",
      "schema": {
        "description": "Any data type is allowed."
      }
    }
  ],
  "returns": {
    "description": "`true` if the data is valid, otherwise `false`.",
    "schema": {
      "type": "boolean"
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 1
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "Test"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": null
      },
      "returns": false
    },
    {
      "arguments": {
        "x": [
          null,
          null
        ]
      },
      "returns": true
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/4610935",
      "title": "IEEE Standard 754-2008 for Floating-Point Arithmetic"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["lt"] = {
  "id": "lt",
  "summary": "Less than comparison",
  "description": "Compares whether `x` is strictly less than `y`.\n\n**Remarks:**\n\n* If any operand is `null`, the return value is `null`.\n* If any operand is an array or object, the return value is `false`.\n* If any operand is not a `number` or temporal string (`date`, `time` or `date-time`), the process returns `false`.\n* Temporal strings can *not* be compared based on their string representation due to the time zone / time-offset representations.",
  "categories": [
    "comparison"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "First operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    },
    {
      "name": "y",
      "description": "Second operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    }
  ],
  "returns": {
    "description": "`true` if `x` is strictly less than `y`, `null` if any operand is `null`, otherwise `false`.",
    "schema": {
      "type": [
        "boolean",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 1,
        "y": null
      },
      "returns": null
    },
    {
      "arguments": {
        "x": 0,
        "y": 0
      },
      "returns": false
    },
    {
      "arguments": {
        "x": 1,
        "y": 2
      },
      "returns": true
    },
    {
      "arguments": {
        "x": -0.5,
        "y": -0.6
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "00:00:00+01:00",
        "y": "00:00:00Z"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "1950-01-01T00:00:00Z",
        "y": "2018-01-01T12:00:00Z"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "2018-01-01T12:00:00+00:00",
        "y": "2018-01-01T12:00:00Z"
      },
      "returns": false
    },
    {
      "arguments": {
        "x": 0,
        "y": true
      },
      "returns": false
    },
    {
      "arguments": {
        "x": false,
        "y": true
      },
      "returns": false
    }
  ]
}


PROCESS_DESCRIPTION_DICT["lte"] = {
  "id": "lte",
  "summary": "Less than or equal to comparison",
  "description": "Compares whether `x` is less than or equal to `y`.\n\n**Remarks:**\n\n* If any operand is `null`, the return value is `null`. Therefore, `lte(null, null)` returns `null` instead of `true`.\n* If any operand is an array or object, the return value is `false`.\n* If the operands are not equal (see process ``eq()``) and any of them is not a `number` or temporal string (`date`, `time` or `date-time`), the process returns `false`.\n* Temporal strings can *not* be compared based on their string representation due to the time zone / time-offset representations.",
  "categories": [
    "comparison"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "First operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    },
    {
      "name": "y",
      "description": "Second operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    }
  ],
  "returns": {
    "description": "`true` if `x` is less than or equal to `y`, `null` if any operand is `null`, otherwise `false`.",
    "schema": {
      "type": [
        "boolean",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 1,
        "y": null
      },
      "returns": null
    },
    {
      "arguments": {
        "x": 0,
        "y": 0
      },
      "returns": true
    },
    {
      "arguments": {
        "x": 1,
        "y": 2
      },
      "returns": true
    },
    {
      "arguments": {
        "x": -0.5,
        "y": -0.6
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "00:00:00+01:00",
        "y": "00:00:00Z"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "1950-01-01T00:00:00Z",
        "y": "2018-01-01T12:00:00Z"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "2018-01-01T12:00:00+00:00",
        "y": "2018-01-01T12:00:00Z"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": false,
        "y": true
      },
      "returns": false
    },
    {
      "arguments": {
        "x": [
          1,
          2,
          3
        ],
        "y": [
          1,
          2,
          3
        ]
      },
      "returns": false
    }
  ],
  "process_graph": {
    "eq": {
      "process_id": "eq",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": {
          "from_parameter": "y"
        }
      }
    },
    "lt": {
      "process_id": "lt",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": {
          "from_parameter": "y"
        }
      }
    },
    "or": {
      "process_id": "or",
      "arguments": {
        "x": {
          "from_node": "lt"
        },
        "y": {
          "from_node": "eq"
        }
      },
      "result": true
    }
  }
}


PROCESS_DESCRIPTION_DICT["neq"] = {
  "id": "neq",
  "summary": "Not equal to comparison",
  "description": "Compares whether `x` is *not* strictly equal to `y`.\n\n**Remarks:**\n\n* Data types MUST be checked strictly. For example, a string with the content *1* is not equal to the number *1*. Nevertheless, an integer *1* is equal to a floating-point number *1.0* as `integer` is a sub-type of `number`.\n* If any operand is `null`, the return value is `null`. Therefore, `neq(null, null)` returns `null` instead of `false`.\n* If any operand is an array or object, the return value is `false`.\n* Strings are expected to be encoded in UTF-8 by default.\n* Temporal strings MUST be compared differently than other strings and MUST NOT be compared based on their string representation due to different possible representations. For example, the time zone representation `Z` (for UTC) has the same meaning as `+00:00`.",
  "categories": [
    "texts",
    "comparison"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "First operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    },
    {
      "name": "y",
      "description": "Second operand.",
      "schema": {
        "description": "Any data type is allowed."
      }
    },
    {
      "name": "delta",
      "description": "Only applicable for comparing two numbers. If this optional parameter is set to a positive non-zero number the non-equality of two numbers is checked against a delta value. This is especially useful to circumvent problems with floating-point inaccuracy in machine-based computation.\n\nThis option is basically an alias for the following computation: `gt(abs(minus([x, y]), delta)`",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      },
      "default": null,
      "optional": true
    },
    {
      "name": "case_sensitive",
      "description": "Only applicable for comparing two strings. Case sensitive comparison can be disabled by setting this parameter to `false`.",
      "schema": {
        "type": "boolean"
      },
      "default": true,
      "optional": true
    }
  ],
  "returns": {
    "description": "`true` if `x` is *not* equal to `y`, `null` if any operand is `null`, otherwise `false`.",
    "schema": {
      "type": [
        "boolean",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 1,
        "y": null
      },
      "returns": null
    },
    {
      "arguments": {
        "x": 1,
        "y": 1
      },
      "returns": false
    },
    {
      "arguments": {
        "x": 1,
        "y": "1"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": 0,
        "y": false
      },
      "returns": true
    },
    {
      "arguments": {
        "x": 1.02,
        "y": 1,
        "delta": 0.01
      },
      "returns": true
    },
    {
      "arguments": {
        "x": -1,
        "y": -1.001,
        "delta": 0.01
      },
      "returns": false
    },
    {
      "arguments": {
        "x": 115,
        "y": 110,
        "delta": 10
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "Test",
        "y": "test"
      },
      "returns": true
    },
    {
      "arguments": {
        "x": "Test",
        "y": "test",
        "case_sensitive": false
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "Ä",
        "y": "ä",
        "case_sensitive": false
      },
      "returns": false
    },
    {
      "arguments": {
        "x": "00:00:00+00:00",
        "y": "00:00:00Z"
      },
      "returns": false
    },
    {
      "description": "`y` is not a valid date-time representation and therefore will be treated as a string so that the provided values are not equal.",
      "arguments": {
        "x": "2018-01-01T12:00:00Z",
        "y": "2018-01-01T12:00:00"
      },
      "returns": true
    },
    {
      "description": "01:00 in the time zone +1 is equal to 00:00 in UTC.",
      "arguments": {
        "x": "2018-01-01T00:00:00Z",
        "y": "2018-01-01T01:00:00+01:00"
      },
      "returns": false
    },
    {
      "arguments": {
        "x": [
          1,
          2,
          3
        ],
        "y": [
          1,
          2,
          3
        ]
      },
      "returns": false
    }
  ],
  "process_graph": {
    "eq": {
      "process_id": "eq",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": {
          "from_parameter": "y"
        },
        "delta": {
          "from_parameter": "delta"
        },
        "case_sensitive": {
          "from_parameter": "case_sensitive"
        }
      }
    },
    "not": {
      "process_id": "not",
      "arguments": {
        "x": {
          "from_node": "eq"
        }
      },
      "result": true
    }
  }
}
