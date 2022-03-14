# -*- coding: utf-8 -*-
from .base import PROCESS_DESCRIPTION_DICT

__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2022, Markus Metz, mundialis"
__maintainer__ = "Markus Metz"
__email__ = "metz@mundialis.de"

# dummy math processes
# these processes do not take a datacube as input, but one or more numbers


PROCESS_DESCRIPTION_DICT["absolute"] = {
  "id": "absolute",
  "summary": "Absolute value",
  "description": "Computes the absolute value of a real number `x`, which is the \"unsigned\" portion of x and often denoted as *|x|*.\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "math"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed absolute value.",
    "schema": {
      "type": [
        "number",
        "null"
      ],
      "minimum": 0
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 0
      },
      "returns": 0
    },
    {
      "arguments": {
        "x": 3.5
      },
      "returns": 3.5
    },
    {
      "arguments": {
        "x": -0.4
      },
      "returns": 0.4
    },
    {
      "arguments": {
        "x": -3.5
      },
      "returns": 3.5
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/AbsoluteValue.html",
      "title": "Absolute value explained by Wolfram MathWorld"
    }
  ],
  "process_graph": {
    "lt": {
      "process_id": "lt",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": 0
      }
    },
    "multiply": {
      "process_id": "multiply",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": -1
      }
    },
    "if": {
      "process_id": "if",
      "arguments": {
        "value": {
          "from_node": "lt"
        },
        "accept": {
          "from_node": "multiply"
        },
        "reject": {
          "from_parameter": "x"
        }
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["add"] = {
  "id": "add",
  "summary": "Addition of two numbers",
  "description": "Sums up the two numbers `x` and `y` (*`x + y`*) and returns the computed sum.\n\nNo-data values are taken into account so that `null` is returned if any element is such a value.\n\nThe computations follow [IEEE Standard 754](https://ieeexplore.ieee.org/document/8766229) whenever the processing environment supports it.",
  "categories": [
    "math"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "The first summand.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    },
    {
      "name": "y",
      "description": "The second summand.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed sum of the two numbers.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 5,
        "y": 2.5
      },
      "returns": 7.5
    },
    {
      "arguments": {
        "x": -2,
        "y": -4
      },
      "returns": -6
    },
    {
      "arguments": {
        "x": 1,
        "y": "null"
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Sum.html",
      "title": "Sum explained by Wolfram MathWorld"
    },
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/8766229",
      "title": "IEEE Standard 754-2019 for Floating-Point Arithmetic"
    }
  ],
  "process_graph": {
    "sum": {
      "process_id": "sum",
      "arguments": {
        "data": [
          {
            "from_parameter": "x"
          },
          {
            "from_parameter": "y"
          }
        ],
        "ignore_nodata": False
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["ceil"] = {
  "id": "ceil",
  "summary": "Round fractions up",
  "description": "The least integer greater than or equal to the number `x`.\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "math > rounding"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number to round up.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The number rounded up.",
    "schema": {
      "type": [
        "integer",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 0
      },
      "returns": 0
    },
    {
      "arguments": {
        "x": 3.5
      },
      "returns": 4
    },
    {
      "arguments": {
        "x": -0.4
      },
      "returns": 0
    },
    {
      "arguments": {
        "x": -3.5
      },
      "returns": -3
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/CeilingFunction.html",
      "title": "Ceiling explained by Wolfram MathWorld"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["clip"] = {
  "id": "clip",
  "summary": "Clip a value between a minimum and a maximum",
  "description": "Clips a number between specified minimum and maximum values. A value larger than the maximum value is set to the maximum value, a value lower than the minimum value is set to the minimum value.\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "math"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    },
    {
      "name": "min",
      "description": "Minimum value. If the value is lower than this value, the process will return the value of this parameter.",
      "schema": {
        "type": "number"
      }
    },
    {
      "name": "max",
      "description": "Maximum value. If the value is greater than this value, the process will return the value of this parameter.",
      "schema": {
        "type": "number"
      }
    }
  ],
  "returns": {
    "description": "The value clipped to the specified range.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": -5,
        "min": -1,
        "max": 1
      },
      "returns": -1
    },
    {
      "arguments": {
        "x": 10.001,
        "min": 1,
        "max": 10
      },
      "returns": 10
    },
    {
      "arguments": {
        "x": 0.000001,
        "min": 0,
        "max": 0.02
      },
      "returns": 0.000001
    },
    {
      "arguments": {
        "x": "null",
        "min": 0,
        "max": 1
      },
      "returns": "null"
    }
  ],
  "process_graph": {
    "min": {
      "process_id": "min",
      "arguments": {
        "data": [
          {
            "from_parameter": "max"
          },
          {
            "from_parameter": "x"
          }
        ]
      }
    },
    "max": {
      "process_id": "max",
      "arguments": {
        "data": [
          {
            "from_parameter": "min"
          },
          {
            "from_node": "min"
          }
        ]
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["cos"] = {
    "id": "cos",
    "summary": "Cosine",
    "description": "Computes the cosine of `x`.\n\nWorks on radians only.\nThe no-data value `null` is passed through and therefore gets propagated.",
    "categories": [
        "math > trigonometric"
    ],
    "parameters": [
        {
            "name": "x",
            "description": "An angle in radians.",
            "schema": {
                "type": [
                    "number",
                    "null"
                ]
            }
        }
    ],
    "returns": {
        "description": "The computed cosine of `x`.",
        "schema": {
            "type": [
                "number",
                "null"
            ]
        }
    },
    "examples": [
        {
            "arguments": {
                "x": 0
            },
            "returns": 1
        }
    ],
    "links": [
        {
            "rel": "about",
            "href": "http://mathworld.wolfram.com/Cosine.html",
            "title": "Cosine explained by Wolfram MathWorld"
        }
    ]
}


PROCESS_DESCRIPTION_DICT["divide"] = {
  "id": "divide",
  "summary": "Division of two numbers",
  "description": "Divides argument `x` by the argument `y` (*`x / y`*) and returns the computed result.\n\nNo-data values are taken into account so that `null` is returned if any element is such a value.\n\nThe computations follow [IEEE Standard 754](https://ieeexplore.ieee.org/document/8766229) whenever the processing environment supports it. Therefore, a division by zero results in ±infinity if the processing environment supports it. Otherwise, a `DivisionByZero` exception must the thrown.",
  "categories": [
    "math"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "The dividend.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    },
    {
      "name": "y",
      "description": "The divisor.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed result.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "exceptions": {
    "DivisionByZero": {
      "message": "Division by zero is not supported."
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 5,
        "y": 2.5
      },
      "returns": 2
    },
    {
      "arguments": {
        "x": -2,
        "y": 4
      },
      "returns": -0.5
    },
    {
      "arguments": {
        "x": 1,
        "y": "null"
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Division.html",
      "title": "Division explained by Wolfram MathWorld"
    },
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/8766229",
      "title": "IEEE Standard 754-2019 for Floating-Point Arithmetic"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["exp"] = {
  "id": "exp",
  "summary": "Exponentiation to the base e",
  "description": "Exponential function to the base *e* raised to the power of `p`.\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "math > exponential & logarithmic"
  ],
  "parameters": [
    {
      "name": "p",
      "description": "The numerical exponent.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed value for *e* raised to the power of `p`.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "p": 0
      },
      "returns": 1
    },
    {
      "arguments": {
        "p": "null"
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/ExponentialFunction.html",
      "title": "Exponential function explained by Wolfram MathWorld"
    }
  ],
  "process_graph": {
    "e": {
      "process_id": "e",
      "arguments": {}
    },
    "power": {
      "process_id": "power",
      "arguments": {
        "base": {
          "from_node": "e"
        },
        "p": {
          "from_parameter": "p"
        }
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["floor"] = {
  "id": "floor",
  "summary": "Round fractions down",
  "description": "The greatest integer less than or equal to the number `x`.\n\nThis process is *not* an alias for the ``int()`` process as defined by some mathematicians, see the examples for negative numbers in both processes for differences.\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "math > rounding"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number to round down.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The number rounded down.",
    "schema": {
      "type": [
        "integer",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 0
      },
      "returns": 0
    },
    {
      "arguments": {
        "x": 3.5
      },
      "returns": 3
    },
    {
      "arguments": {
        "x": -0.4
      },
      "returns": -1
    },
    {
      "arguments": {
        "x": -3.5
      },
      "returns": -4
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/FloorFunction.html",
      "title": "Floor explained by Wolfram MathWorld"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["int"] = {
  "id": "int",
  "summary": "Integer part of a number",
  "description": "The integer part of the real number `x`.\n\nThis process is *not* an alias for the ``floor()`` process as defined by some mathematicians, see the examples for negative numbers in both processes for differences.\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "math",
    "math > rounding"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "Integer part of the number.",
    "schema": {
      "type": [
        "integer",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 0
      },
      "returns": 0
    },
    {
      "arguments": {
        "x": 3.5
      },
      "returns": 3
    },
    {
      "arguments": {
        "x": -0.4
      },
      "returns": 0
    },
    {
      "arguments": {
        "x": -3.5
      },
      "returns": -3
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/IntegerPart.html",
      "title": "Integer Part explained by Wolfram MathWorld"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["linear_scale_range"] = {
  "id": "linear_scale_range",
  "summary": "Linear transformation between two ranges",
  "description": "Performs a linear transformation between the input and output range.\n\nThe given number in `x` is clipped to the bounds specified in `inputMin` and `inputMax` so that the underlying formula *`((x - inputMin) / (inputMax - inputMin)) * (outputMax - outputMin) + outputMin`* never returns any value lower than `outputMin` or greater than `outputMax`.\n\nPotential use case include\n\n* scaling values to the 8-bit range (0 - 255) often used for numeric representation of values in one of the channels of the [RGB colour model](https://en.wikipedia.org/wiki/RGB_color_model#Numeric_representations) or\n* calculating percentages (0 - 100).\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "math"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number to transform. The number gets clipped to the bounds specified in `inputMin` and `inputMax`.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    },
    {
      "name": "inputMin",
      "description": "Minimum value the input can obtain.",
      "schema": {
        "type": "number"
      }
    },
    {
      "name": "inputMax",
      "description": "Maximum value the input can obtain.",
      "schema": {
        "type": "number"
      }
    },
    {
      "name": "outputMin",
      "description": "Minimum value of the desired output range.",
      "schema": {
        "type": "number"
      },
      "default": 0,
      "optional": True
    },
    {
      "name": "outputMax",
      "description": "Maximum value of the desired output range.",
      "schema": {
        "type": "number"
      },
      "default": 1,
      "optional": True
    }
  ],
  "returns": {
    "description": "The transformed number.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 0.3,
        "inputMin": -1,
        "inputMax": 1,
        "outputMin": 0,
        "outputMax": 255
      },
      "returns": 165.75
    },
    {
      "arguments": {
        "x": 25.5,
        "inputMin": 0,
        "inputMax": 255
      },
      "returns": 0.1
    },
    {
      "arguments": {
        "x": "null",
        "inputMin": 0,
        "inputMax": 100
      },
      "returns": "null"
    },
    {
      "description": "Shows that the input data is clipped.",
      "arguments": {
        "x": 1.12,
        "inputMin": 0,
        "inputMax": 1,
        "outputMin": 0,
        "outputMax": 255
      },
      "returns": 255
    }
  ],
  "process_graph": {
    "subtract1": {
      "process_id": "subtract",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": {
          "from_parameter": "inputMin"
        }
      }
    },
    "subtract2": {
      "process_id": "subtract",
      "arguments": {
        "x": {
          "from_parameter": "inputMax"
        },
        "y": {
          "from_parameter": "inputMin"
        }
      }
    },
    "subtract3": {
      "process_id": "subtract",
      "arguments": {
        "x": {
          "from_parameter": "outputMax"
        },
        "y": {
          "from_parameter": "outputMin"
        }
      }
    },
    "divide": {
      "process_id": "divide",
      "arguments": {
        "x": {
          "from_node": "subtract1"
        },
        "y": {
          "from_node": "subtract2"
        }
      }
    },
    "multiply": {
      "process_id": "multiply",
      "arguments": {
        "x": {
          "from_node": "divide"
        },
        "y": {
          "from_node": "subtract3"
        }
      }
    },
    "add": {
      "process_id": "add",
      "arguments": {
        "x": {
          "from_node": "multiply"
        },
        "y": {
          "from_parameter": "outputMin"
        }
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["ln"] = {
  "id": "ln",
  "summary": "Natural logarithm",
  "description": "The natural logarithm is the logarithm to the base *e* of the number `x`, which equals to using the *log* process with the base set to *e*. The natural logarithm is the inverse function of taking *e* to the power x.\n\nThe no-data value `null` is passed through.\n\nThe computations follow [IEEE Standard 754](https://ieeexplore.ieee.org/document/8766229) whenever the processing environment supports it. Therefore, *`ln(0)`* results in ±infinity if the processing environment supports it or otherwise an exception is thrown.",
  "categories": [
    "math > exponential & logarithmic"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number to compute the natural logarithm for.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed natural logarithm.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 1
      },
      "returns": 0
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/NaturalLogarithm.html",
      "title": "Natural logarithm explained by Wolfram MathWorld"
    },
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/8766229",
      "title": "IEEE Standard 754-2019 for Floating-Point Arithmetic"
    }
  ],
  "process_graph": {
    "e": {
      "process_id": "e",
      "arguments": {}
    },
    "log": {
      "process_id": "log",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "base": {
          "from_node": "e"
        }
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["log"] = {
  "id": "log",
  "summary": "Logarithm to a base",
  "description": "Logarithm to the base `base` of the number `x` is defined to be the inverse function of taking b to the power of x.\n\nThe no-data value `null` is passed through and therefore gets propagated if any of the arguments is `null`.\n\nThe computations follow [IEEE Standard 754](https://ieeexplore.ieee.org/document/8766229) whenever the processing environment supports it. Therefore, `log(0, 2)` results in ±infinity if the processing environment supports it or otherwise an exception is thrown.",
  "categories": [
    "math > exponential & logarithmic"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number to compute the logarithm for.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    },
    {
      "name": "base",
      "description": "The numerical base.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed logarithm.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 10,
        "base": 10
      },
      "returns": 1
    },
    {
      "arguments": {
        "x": 2,
        "base": 2
      },
      "returns": 1
    },
    {
      "arguments": {
        "x": 4,
        "base": 2
      },
      "returns": 2
    },
    {
      "arguments": {
        "x": 1,
        "base": 16
      },
      "returns": 0
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Logarithm.html",
      "title": "Logarithm explained by Wolfram MathWorld"
    },
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/8766229",
      "title": "IEEE Standard 754-2019 for Floating-Point Arithmetic"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["max"] = {
  "id": "max",
  "summary": "Maximum value",
  "description": "Computes the largest value of an array of numbers, which is equal to the first element of a sorted (i.e., ordered) version of the array.\n\nAn array without non-`null` elements resolves always with `null`.",
  "categories": [
    "math",
    "math > statistics",
    "reducer"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "An array of numbers.",
      "schema": {
        "type": "array",
        "items": {
          "type": [
            "number",
            "null"
          ]
        }
      }
    },
    {
      "name": "ignore_nodata",
      "description": "Indicates whether no-data values are ignored or not. Ignores them by default. Setting this flag to `false` considers no-data values so that `null` is returned if any value is such a value.",
      "schema": {
        "type": "boolean"
      },
      "default": True,
      "optional": True
    }
  ],
  "returns": {
    "description": "The maximum value.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "data": [
          1,
          0,
          3,
          2
        ]
      },
      "returns": 3
    },
    {
      "arguments": {
        "data": [
          5,
          2.5,
          "null",
          -0.7
        ]
      },
      "returns": 5
    },
    {
      "arguments": {
        "data": [
          1,
          0,
          3,
          "null",
          2
        ],
        "ignore_nodata": False
      },
      "returns": "null"
    },
    {
      "description": "The input array is empty: return `null`.",
      "arguments": {
        "data": []
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Maximum.html",
      "title": "Maximum explained by Wolfram MathWorld"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["mean"] = {
  "id": "mean",
  "summary": "Arithmetic mean (average)",
  "description": "The arithmetic mean of an array of numbers is the quantity commonly called the average. It is defined as the sum of all elements divided by the number of elements.\n\nAn array without non-`null` elements resolves always with `null`.",
  "categories": [
    "math > statistics",
    "reducer"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "An array of numbers.",
      "schema": {
        "type": "array",
        "items": {
          "type": [
            "number",
            "null"
          ]
        }
      }
    },
    {
      "name": "ignore_nodata",
      "description": "Indicates whether no-data values are ignored or not. Ignores them by default. Setting this flag to `false` considers no-data values so that `null` is returned if any value is such a value.",
      "schema": {
        "type": "boolean"
      },
      "default": True,
      "optional": True
    }
  ],
  "returns": {
    "description": "The computed arithmetic mean.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "data": [
          1,
          0,
          3,
          2
        ]
      },
      "returns": 1.5
    },
    {
      "arguments": {
        "data": [
          9,
          2.5,
          "null",
          -2.5
        ]
      },
      "returns": 3
    },
    {
      "arguments": {
        "data": [
          1,
          "null"
        ],
        "ignore_nodata": False
      },
      "returns": "null"
    },
    {
      "description": "The input array is empty: return `null`.",
      "arguments": {
        "data": []
      },
      "returns": "null"
    },
    {
      "description": "The input array has only `null` elements: return `null`.",
      "arguments": {
        "data": [
          "null",
          "null"
        ]
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/ArithmeticMean.html",
      "title": "Arithmetic mean explained by Wolfram MathWorld"
    }
  ],
  "process_graph": {
    "count_condition": {
      "process_id": "if",
      "arguments": {
        "value": {
          "from_parameter": "ignore_nodata"
        },
        "accept": "null",
        "reject": True
      }
    },
    "count": {
      "process_id": "count",
      "arguments": {
        "data": {
          "from_parameter": "data"
        },
        "condition": {
          "from_node": "count_condition"
        }
      }
    },
    "sum": {
      "process_id": "sum",
      "arguments": {
        "data": {
          "from_parameter": "data"
        },
        "ignore_nodata": {
          "from_parameter": "ignore_nodata"
        }
      }
    },
    "divide": {
      "process_id": "divide",
      "arguments": {
        "x": {
          "from_node": "sum"
        },
        "y": {
          "from_node": "count"
        }
      }
    },
    "neq": {
      "process_id": "neq",
      "arguments": {
        "x": {
          "from_node": "count"
        },
        "y": 0
      }
    },
    "if": {
      "process_id": "if",
      "arguments": {
        "value": {
          "from_node": "neq"
        },
        "accept": {
          "from_node": "divide"
        }
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["min"] = {
  "id": "min",
  "summary": "Minimum value",
  "description": "Computes the smallest value of an array of numbers, which is equal to the last element of a sorted (i.e., ordered) version of the array.\n\nAn array without non-`null` elements resolves always with `null`.",
  "categories": [
    "math",
    "math > statistics",
    "reducer"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "An array of numbers.",
      "schema": {
        "type": "array",
        "items": {
          "type": [
            "number",
            "null"
          ]
        }
      }
    },
    {
      "name": "ignore_nodata",
      "description": "Indicates whether no-data values are ignored or not. Ignores them by default. Setting this flag to `false` considers no-data values so that `null` is returned if any value is such a value.",
      "schema": {
        "type": "boolean"
      },
      "default": True,
      "optional": True
    }
  ],
  "returns": {
    "description": "The minimum value.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "data": [
          1,
          0,
          3,
          2
        ]
      },
      "returns": 0
    },
    {
      "arguments": {
        "data": [
          5,
          2.5,
          "null",
          -0.7
        ]
      },
      "returns": -0.7
    },
    {
      "arguments": {
        "data": [
          1,
          0,
          3,
          "null",
          2
        ],
        "ignore_nodata": False
      },
      "returns": "null"
    },
    {
      "arguments": {
        "data": []
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Minimum.html",
      "title": "Minimum explained by Wolfram MathWorld"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["mod"] = {
  "id": "mod",
  "summary": "Modulo",
  "description": "Remainder after a division of `x` by `y` for both integers and floating-point numbers.\n\nThe result of a modulo operation has the sign of the divisor. The handling regarding the sign of the result [differs between programming languages](https://en.wikipedia.org/wiki/Modulo_operation#In_programming_languages) and needs careful consideration to avoid unexpected results.\n\nThe no-data value `null` is passed through and therefore gets propagated if any of the arguments is `null`. A modulo by zero results in ±infinity if the processing environment supports it. Otherwise, a `DivisionByZero` exception must the thrown.",
  "categories": [
    "math"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number to be used as the dividend.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    },
    {
      "name": "y",
      "description": "A number to be used as the divisor.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The remainder after division.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "exceptions": {
    "DivisionByZero": {
      "message": "Division by zero is not supported."
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 27,
        "y": 5
      },
      "returns": 2
    },
    {
      "arguments": {
        "x": -27,
        "y": 5
      },
      "returns": 3
    },
    {
      "arguments": {
        "x": 3.14,
        "y": -2
      },
      "returns": -0.86
    },
    {
      "arguments": {
        "x": -27,
        "y": -5
      },
      "returns": -2
    },
    {
      "arguments": {
        "x": 27,
        "y": "null"
      },
      "returns": "null"
    },
    {
      "arguments": {
        "x": "null",
        "y": 5
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "https://en.wikipedia.org/wiki/Modulo_operation",
      "title": "Modulo explained by Wikipedia"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["multiply"] = {
  "id": "multiply",
  "summary": "Multiplication of two numbers",
  "description": "Multiplies the two numbers `x` and `y` (*`x * y`*) and returns the computed product.\n\nNo-data values are taken into account so that `null` is returned if any element is such a value.\n\nThe computations follow [IEEE Standard 754](https://ieeexplore.ieee.org/document/8766229) whenever the processing environment supports it.",
  "categories": [
    "math"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "The multiplier.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    },
    {
      "name": "y",
      "description": "The multiplicand.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed product of the two numbers.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "exceptions": {
    "MultiplicandMissing": {
      "message": "Multiplication requires at least two numbers."
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 5,
        "y": 2.5
      },
      "returns": 12.5
    },
    {
      "arguments": {
        "x": -2,
        "y": -4
      },
      "returns": 8
    },
    {
      "arguments": {
        "x": 1,
        "y": "null"
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Product.html",
      "title": "Product explained by Wolfram MathWorld"
    },
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/8766229",
      "title": "IEEE Standard 754-2019 for Floating-Point Arithmetic"
    }
  ],
  "process_graph": {
    "product": {
      "process_id": "product",
      "arguments": {
        "data": [
          {
            "from_parameter": "x"
          },
          {
            "from_parameter": "y"
          }
        ],
        "ignore_nodata": False
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["power"] = {
  "id": "power",
  "summary": "Exponentiation",
  "description": "Computes the exponentiation for the base `base` raised to the power of `p`.\n\nThe no-data value `null` is passed through and therefore gets propagated if any of the arguments is `null`.",
  "categories": [
    "math",
    "math > exponential & logarithmic"
  ],
  "parameters": [
    {
      "name": "base",
      "description": "The numerical base.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    },
    {
      "name": "p",
      "description": "The numerical exponent.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed value for `base` raised to the power of `p`.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "base": 0,
        "p": 2
      },
      "returns": 0
    },
    {
      "arguments": {
        "base": 2.5,
        "p": 0
      },
      "returns": 1
    },
    {
      "arguments": {
        "base": 3,
        "p": 3
      },
      "returns": 27
    },
    {
      "arguments": {
        "base": 5,
        "p": -1
      },
      "returns": 0.2
    },
    {
      "arguments": {
        "base": 1,
        "p": 0.5
      },
      "returns": 1
    },
    {
      "arguments": {
        "base": 1,
        "p": "null"
      },
      "returns": "null"
    },
    {
      "arguments": {
        "base": "null",
        "p": 2
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Power.html",
      "title": "Power explained by Wolfram MathWorld"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["product"] = {
  "id": "product",
  "summary": "Compute the product by multiplying numbers",
  "description": "Multiplies all elements in a sequential array of numbers and returns the computed product.\n\nBy default no-data values are ignored. Setting `ignore_nodata` to `false` considers no-data values so that `null` is returned if any element is such a value.\n\nThe computations follow [IEEE Standard 754](https://ieeexplore.ieee.org/document/8766229) whenever the processing environment supports it.",
  "categories": [
    "math",
    "reducer"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "An array of numbers.",
      "schema": {
        "type": "array",
        "items": {
          "type": [
            "number",
            "null"
          ]
        }
      }
    },
    {
      "name": "ignore_nodata",
      "description": "Indicates whether no-data values are ignored or not. Ignores them by default. Setting this flag to `false` considers no-data values so that `null` is returned if any value is such a value.",
      "schema": {
        "type": "boolean"
      },
      "default": True,
      "optional": True
    }
  ],
  "returns": {
    "description": "The computed product of the sequence of numbers.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "data": [
          5,
          0
        ]
      },
      "returns": 0
    },
    {
      "arguments": {
        "data": [
          -2,
          4,
          2.5
        ]
      },
      "returns": -20
    },
    {
      "arguments": {
        "data": [
          1,
          "null"
        ],
        "ignore_nodata": False
      },
      "returns": "null"
    },
    {
      "arguments": {
        "data": [
          -1
        ]
      },
      "returns": -1
    },
    {
      "arguments": {
        "data": [
          "null"
        ],
        "ignore_nodata": False
      },
      "returns": "null"
    },
    {
      "arguments": {
        "data": []
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Product.html",
      "title": "Product explained by Wolfram MathWorld"
    },
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/8766229",
      "title": "IEEE Standard 754-2019 for Floating-Point Arithmetic"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["quantiles"] = {
  "id": "quantiles",
  "summary": "Quantiles",
  "description": "Calculates quantiles, which are cut points dividing the range of a sample distribution into either\n\n* intervals corresponding to the given `probabilities` or\n* equal-sized intervals (q-quantiles based on the parameter `q`).\n\nEither the parameter `probabilities` or `q` must be specified, otherwise the `QuantilesParameterMissing` exception is thrown. If both parameters are set the `QuantilesParameterConflict` exception is thrown.\n\nSample quantiles can be computed with several different algorithms. Hyndman and Fan (1996) have concluded on nine different types, which are commonly implemented in statistical software packages. This process is implementing type 7, which is implemented widely and often also the default type (e.g. in Excel, Julia, Python, R and S).",
  "categories": [
    "math > statistics"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "An array of numbers.",
      "schema": {
        "type": "array",
        "items": {
          "type": [
            "number",
            "null"
          ]
        }
      }
    },
    {
      "name": "probabilities",
      "description": "A list of probabilities to calculate quantiles for. The probabilities must be between 0 and 1 (inclusive).",
      "schema": {
        "type": "array",
        "items": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        }
      },
      "optional": True
    },
    {
      "name": "q",
      "description": "Number of intervals to calculate quantiles for. Calculates q-quantiles with equal-sized intervals.",
      "schema": {
        "type": "integer",
        "minimum": 2
      },
      "optional": True
    },
    {
      "name": "ignore_nodata",
      "description": "Indicates whether no-data values are ignored or not. Ignores them by default. Setting this flag to `false` considers no-data values so that an array with `null` values is returned if any element is such a value.",
      "schema": {
        "type": "boolean"
      },
      "default": True,
      "optional": True
    }
  ],
  "returns": {
    "description": "An array with the computed quantiles. The list has either\n\n* as many elements as the given list of `probabilities` had or\n* *`q`-1* elements.\n\nIf the input array is empty the resulting array is filled with as many `null` values as required according to the list above. See the 'Empty array' example for an example.",
    "schema": {
      "type": "array",
      "items": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  },
  "exceptions": {
    "QuantilesParameterMissing": {
      "message": "The process `quantiles` requires either the `probabilities` or `q` parameter to be set."
    },
    "QuantilesParameterConflict": {
      "message": "The process `quantiles` only allows that either the `probabilities` or the `q` parameter is set."
    }
  },
  "examples": [
    {
      "arguments": {
        "data": [
          2,
          4,
          4,
          4,
          5,
          5,
          7,
          9
        ],
        "probabilities": [
          0.005,
          0.01,
          0.02,
          0.05,
          0.1,
          0.5
        ]
      },
      "returns": [
        2.07,
        2.14,
        2.28,
        2.7,
        3.4,
        4.5
      ]
    },
    {
      "arguments": {
        "data": [
          2,
          4,
          4,
          4,
          5,
          5,
          7,
          9
        ],
        "q": 4
      },
      "returns": [
        4,
        4.5,
        5.5
      ]
    },
    {
      "arguments": {
        "data": [
          -1,
          -0.5,
          "null",
          1
        ],
        "q": 2
      },
      "returns": [
        -0.5
      ]
    },
    {
      "arguments": {
        "data": [
          -1,
          -0.5,
          "null",
          1
        ],
        "q": 4,
        "ignore_nodata": False
      },
      "returns": [
        "null",
        "null",
        "null"
      ]
    },
    {
      "title": "Empty array",
      "arguments": {
        "data": [],
        "probabilities": [
          0.1,
          0.5
        ]
      },
      "returns": [
        "null",
        "null"
      ]
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "https://en.wikipedia.org/wiki/Quantile",
      "title": "Quantiles explained by Wikipedia"
    },
    {
      "rel": "about",
      "href": "https://www.amherst.edu/media/view/129116/original/Sample+Quantiles.pdf",
      "type": "application/pdf",
      "title": "Hyndman and Fan (1996): Sample Quantiles in Statistical Packages"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["round"] = {
  "id": "round",
  "summary": "Round to a specified precision",
  "description": "Rounds a real number `x` to specified precision `p`.\n\nIf the fractional part of `x` is halfway between two integers, one of which is even and the other odd, then the even number is returned.\nThis behavior follows [IEEE Standard 754](https://ieeexplore.ieee.org/document/8766229). This kind of rounding is also called \"round to nearest (even)\" or \"banker's rounding\". It minimizes rounding errors that result from consistently rounding a midpoint value in a single direction.\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "math > rounding"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number to round.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    },
    {
      "name": "p",
      "description": "A positive number specifies the number of digits after the decimal point to round to. A negative number means rounding to a power of ten, so for example *-2* rounds to the nearest hundred. Defaults to *0*.",
      "schema": {
        "type": "integer"
      },
      "default": 0,
      "optional": True
    }
  ],
  "returns": {
    "description": "The rounded number.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 0
      },
      "returns": 0
    },
    {
      "arguments": {
        "x": 3.56,
        "p": 1
      },
      "returns": 3.6
    },
    {
      "arguments": {
        "x": -0.4444444,
        "p": 2
      },
      "returns": -0.44
    },
    {
      "arguments": {
        "x": -2.5
      },
      "returns": -2
    },
    {
      "arguments": {
        "x": -3.5
      },
      "returns": -4
    },
    {
      "arguments": {
        "x": 1234.5,
        "p": -2
      },
      "returns": 1200
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/AbsoluteValue.html",
      "title": "Absolute value explained by Wolfram MathWorld"
    },
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/8766229",
      "title": "IEEE Standard 754-2019 for Floating-Point Arithmetic"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["sd"] = {
  "id": "sd",
  "summary": "Standard deviation",
  "description": "Computes the sample standard deviation, which quantifies the amount of variation of an array of numbers. It is defined to be the square root of the corresponding variance (see ``variance()``).\n\nA low standard deviation indicates that the values tend to be close to the expected value, while a high standard deviation indicates that the values are spread out over a wider range.\n\nAn array without non-`null` elements resolves always with `null`.",
  "categories": [
    "math > statistics",
    "reducer"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "An array of numbers.",
      "schema": {
        "type": "array",
        "items": {
          "type": [
            "number",
            "null"
          ]
        }
      }
    },
    {
      "name": "ignore_nodata",
      "description": "Indicates whether no-data values are ignored or not. Ignores them by default. Setting this flag to `false` considers no-data values so that `null` is returned if any value is such a value.",
      "schema": {
        "type": "boolean"
      },
      "default": True,
      "optional": True
    }
  ],
  "returns": {
    "description": "The computed sample standard deviation.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "data": [
          -1,
          1,
          3,
          "null"
        ]
      },
      "returns": 2
    },
    {
      "arguments": {
        "data": [
          -1,
          1,
          3,
          "null"
        ],
        "ignore_nodata": False
      },
      "returns": "null"
    },
    {
      "description": "The input array is empty: return `null`.",
      "arguments": {
        "data": []
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/StandardDeviation.html",
      "title": "Standard deviation explained by Wolfram MathWorld"
    }
  ],
  "process_graph": {
    "variance": {
      "process_id": "variance",
      "arguments": {
        "data": {
          "from_parameter": "data"
        },
        "ignore_nodata": {
          "from_parameter": "ignore_nodata"
        }
      }
    },
    "power": {
      "process_id": "power",
      "arguments": {
        "base": {
          "from_node": "variance"
        },
        "p": 0.5
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["sgn"] = {
  "id": "sgn",
  "summary": "Signum",
  "description": "The signum (also known as *sign*) of `x` is defined as:\n\n* *1* if *x > 0*\n* *0* if *x = 0*\n* *-1* if *x < 0*\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "math"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed signum value of `x`.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": -2
      },
      "returns": -1
    },
    {
      "arguments": {
        "x": 3.5
      },
      "returns": 1
    },
    {
      "arguments": {
        "x": 0
      },
      "returns": 0
    },
    {
      "arguments": {
        "x": "null"
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Sign.html",
      "title": "Sign explained by Wolfram MathWorld"
    }
  ],
  "process_graph": {
    "gt0": {
      "process_id": "gt",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": 0
      }
    },
    "lt0": {
      "process_id": "lt",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": 0
      }
    },
    "if_gt0": {
      "process_id": "if",
      "arguments": {
        "value": {
          "from_node": "gt0"
        },
        "accept": 1,
        "reject": {
          "from_parameter": "x"
        }
      }
    },
    "if_lt0": {
      "process_id": "if",
      "arguments": {
        "value": {
          "from_node": "lt0"
        },
        "accept": -1,
        "reject": {
          "from_node": "if_gt0"
        }
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["sin"] = {
    "id": "sin",
    "summary": "Sine",
    "description": "Computes the sine of `x`.\n\nWorks on radians only.\nThe no-data value `null` is passed through and therefore gets propagated.",
    "categories": [
        "math > trigonometric"
    ],
    "parameters": [
        {
            "name": "x",
            "description": "An angle in radians.",
            "schema": {
                "type": [
                    "number",
                    "null"
                ]
            }
        }
    ],
    "returns": {
        "description": "The computed sine of `x`.",
        "schema": {
            "type": [
                "number",
                "null"
            ]
        }
    },
    "examples": [
        {
            "arguments": {
                "x": 0
            },
            "returns": 0
        }
    ],
    "links": [
        {
            "rel": "about",
            "href": "http://mathworld.wolfram.com/Sine.html",
            "title": "Sine explained by Wolfram MathWorld"
        }
    ]
}


PROCESS_DESCRIPTION_DICT["sqrt"] = {
  "id": "sqrt",
  "summary": "Square root",
  "description": "Computes the square root of a real number `x`, which is equal to calculating `x` to the power of *0.5*.\n\nA square root of x is a number a such that *`a² = x`*. Therefore, the square root is the inverse function of a to the power of 2, but only for *a >= 0*.\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "math",
    "math > exponential & logarithmic"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A number.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed square root.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 0
      },
      "returns": 0
    },
    {
      "arguments": {
        "x": 1
      },
      "returns": 1
    },
    {
      "arguments": {
        "x": 9
      },
      "returns": 3
    },
    {
      "arguments": {
        "x": "null"
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/SquareRoot.html",
      "title": "Square root explained by Wolfram MathWorld"
    }
  ],
  "process_graph": {
    "power": {
      "process_id": "power",
      "arguments": {
        "base": {
          "from_parameter": "x"
        },
        "p": 0.5
      },
      "result": True
    }
  }
}


PROCESS_DESCRIPTION_DICT["subtract"] = {
  "id": "subtract",
  "summary": "Subtraction of two numbers",
  "description": "Subtracts argument `y` from the argument `x` (*`x - y`*) and returns the computed result.\n\nNo-data values are taken into account so that `null` is returned if any element is such a value.\n\nThe computations follow [IEEE Standard 754](https://ieeexplore.ieee.org/document/8766229) whenever the processing environment supports it.",
  "categories": [
    "math"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "The minuend.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    },
    {
      "name": "y",
      "description": "The subtrahend.",
      "schema": {
        "type": [
          "number",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "The computed result.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "x": 5,
        "y": 2.5
      },
      "returns": 2.5
    },
    {
      "arguments": {
        "x": -2,
        "y": 4
      },
      "returns": -6
    },
    {
      "arguments": {
        "x": 1,
        "y": "null"
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Subtraction.html",
      "title": "Subtraction explained by Wolfram MathWorld"
    },
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/8766229",
      "title": "IEEE Standard 754-2019 for Floating-Point Arithmetic"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["sum"] = {
  "id": "sum",
  "summary": "Compute the sum by adding up numbers",
  "description": "Sums up all elements in a sequential array of numbers and returns the computed sum.\n\nBy default no-data values are ignored. Setting `ignore_nodata` to `false` considers no-data values so that `null` is returned if any element is such a value.\n\nThe computations follow [IEEE Standard 754](https://ieeexplore.ieee.org/document/8766229) whenever the processing environment supports it.",
  "categories": [
    "math",
    "reducer"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "An array of numbers.",
      "schema": {
        "type": "array",
        "items": {
          "type": [
            "number",
            "null"
          ]
        }
      }
    },
    {
      "name": "ignore_nodata",
      "description": "Indicates whether no-data values are ignored or not. Ignores them by default. Setting this flag to `false` considers no-data values so that `null` is returned if any value is such a value.",
      "schema": {
        "type": "boolean"
      },
      "default": True,
      "optional": True
    }
  ],
  "returns": {
    "description": "The computed sum of the sequence of numbers.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "data": [
          5,
          1
        ]
      },
      "returns": 6
    },
    {
      "arguments": {
        "data": [
          -2,
          4,
          2.5
        ]
      },
      "returns": 4.5
    },
    {
      "arguments": {
        "data": [
          1,
          "null"
        ],
        "ignore_nodata": False
      },
      "returns": "null"
    },
    {
      "arguments": {
        "data": [
          100
        ]
      },
      "returns": 100
    },
    {
      "arguments": {
        "data": [
          "null"
        ],
        "ignore_nodata": False
      },
      "returns": "null"
    },
    {
      "arguments": {
        "data": []
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Sum.html",
      "title": "Sum explained by Wolfram MathWorld"
    },
    {
      "rel": "about",
      "href": "https://ieeexplore.ieee.org/document/8766229",
      "title": "IEEE Standard 754-2019 for Floating-Point Arithmetic"
    }
  ]
}


PROCESS_DESCRIPTION_DICT["variance"] = {
  "id": "variance",
  "summary": "Variance",
  "description": "Computes the sample variance of an array of numbers by calculating the square of the standard deviation (see ``sd()``). It is defined to be the expectation of the squared deviation of a random variable from its expected value. Basically, it measures how far the numbers in the array are spread out from their average value.\n\nAn array without non-`null` elements resolves always with `null`.",
  "categories": [
    "math > statistics",
    "reducer"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "An array of numbers.",
      "schema": {
        "type": "array",
        "items": {
          "type": [
            "number",
            "null"
          ]
        }
      }
    },
    {
      "name": "ignore_nodata",
      "description": "Indicates whether no-data values are ignored or not. Ignores them by default. Setting this flag to `false` considers no-data values so that `null` is returned if any value is such a value.",
      "schema": {
        "type": "boolean"
      },
      "default": True,
      "optional": True
    }
  ],
  "returns": {
    "description": "The computed sample variance.",
    "schema": {
      "type": [
        "number",
        "null"
      ]
    }
  },
  "examples": [
    {
      "arguments": {
        "data": [
          -1,
          1,
          3
        ]
      },
      "returns": 4
    },
    {
      "arguments": {
        "data": [
          2,
          3,
          3,
          "null",
          4,
          4,
          5
        ]
      },
      "returns": 1.1
    },
    {
      "arguments": {
        "data": [
          -1,
          1,
          "null",
          3
        ],
        "ignore_nodata": False
      },
      "returns": "null"
    },
    {
      "description": "The input array is empty: return `null`.",
      "arguments": {
        "data": []
      },
      "returns": "null"
    }
  ],
  "links": [
    {
      "rel": "about",
      "href": "http://mathworld.wolfram.com/Variance.html",
      "title": "Variance explained by Wolfram MathWorld"
    }
  ],
  "process_graph": {
    "mean": {
      "process_id": "mean",
      "arguments": {
        "data": {
          "from_parameter": "data"
        }
      }
    },
    "apply": {
      "process_id": "apply",
      "arguments": {
        "data": {
          "from_parameter": "data"
        },
        "process": {
          "process-graph": {
            "subtract": {
              "process_id": "subtract",
              "arguments": {
                "x": {
                  "from_parameter": "x"
                },
                "y": {
                  "from_parameter": "context"
                }
              }
            },
            "power": {
              "process_id": "power",
              "arguments": {
                "base": {
                  "from_node": "subtract"
                },
                "p": 2
              },
              "result": True
            }
          }
        },
        "context": {
          "from_node": "mean"
        }
      }
    },
    "mean2": {
      "process_id": "mean",
      "arguments": {
        "data": {
          "from_node": "apply"
        },
        "ignore_nodata": {
          "from_parameter": "ignore_nodata"
        }
      },
      "result": True
    }
  }
}
