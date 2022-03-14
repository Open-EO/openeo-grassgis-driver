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

# dummy logic processes
# these processes do not take a datacube as input, but one or more numbers


PROCESS_DESCRIPTION_DICT["all"] = {
  "id": "all",
  "summary": "Are all of the values true?",
  "description": "Checks if **all** of the values in `data` are true. If no value is given (i.e. the array is empty) the process returns `null`.\n\nBy default all no-data values are ignored so that the process returns `null` if all values are no-data, `true` if all values are true and `false` otherwise. Setting the `ignore_nodata` flag to `false` takes no-data values into account and the array values are reduced pairwise according to the following truth table:\n\n```\n      || null  | false | true\n----- || ----- | ----- | -----\nnull  || null  | false | null\nfalse || false | false | false\ntrue  || null  | false | true\n```\n\n**Remark:** The process evaluates all values from the first to the last element and stops once the outcome is unambiguous. A result is ambiguous unless a value is `false` or all values have been taken into account.",
  "categories": [
    "logic",
    "reducer"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "A set of boolean values.",
      "schema": {
        "type": "array",
        "items": {
          "type": [
            "boolean",
            "null"
          ]
        }
      }
    },
    {
      "name": "ignore_nodata",
      "description": "Indicates whether no-data values are ignored or not and ignores them by default.",
      "schema": {
        "type": "boolean"
      },
      "default": true,
      "optional": true
    }
  ],
  "returns": {
    "description": "Boolean result of the logical operation.",
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
        "data": [
          false,
          null
        ]
      },
      "returns": false
    },
    {
      "arguments": {
        "data": [
          true,
          null
        ]
      },
      "returns": true
    },
    {
      "arguments": {
        "data": [
          false,
          null
        ],
        "ignore_nodata": false
      },
      "returns": false
    },
    {
      "arguments": {
        "data": [
          true,
          null
        ],
        "ignore_nodata": false
      },
      "returns": null
    },
    {
      "arguments": {
        "data": [
          true,
          false,
          true,
          false
        ]
      },
      "returns": false
    },
    {
      "arguments": {
        "data": [
          true,
          false
        ]
      },
      "returns": false
    },
    {
      "arguments": {
        "data": [
          true,
          true
        ]
      },
      "returns": true
    },
    {
      "arguments": {
        "data": [
          true
        ]
      },
      "returns": true
    },
    {
      "arguments": {
        "data": [
          null
        ],
        "ignore_nodata": false
      },
      "returns": null
    },
    {
      "arguments": {
        "data": []
      },
      "returns": null
    }
  ]
}


PROCESS_DESCRIPTION_DICT["and"] = {
  "id": "and",
  "summary": "Logical AND",
  "description": "Checks if **both** values are true.\n\nEvaluates parameter `x` before `y` and stops once the outcome is unambiguous. If any argument is `null`, the result will be `null` if the outcome is ambiguous.\n\n**Truth table:**\n\n```\na \\ b || null  | false | true\n----- || ----- | ----- | -----\nnull  || null  | false | null\nfalse || false | false | false\ntrue  || null  | false | true\n```",
  "categories": [
    "logic"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A boolean value.",
      "schema": {
        "type": [
          "boolean",
          "null"
        ]
      }
    },
    {
      "name": "y",
      "description": "A boolean value.",
      "schema": {
        "type": [
          "boolean",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "Boolean result of the logical AND.",
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
        "x": true,
        "y": true
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
        "x": false,
        "y": false
      },
      "returns": false
    },
    {
      "arguments": {
        "x": false,
        "y": null
      },
      "returns": false
    },
    {
      "arguments": {
        "x": true,
        "y": null
      },
      "returns": null
    }
  ],
  "process_graph": {
    "all": {
      "process_id": "all",
      "arguments": {
        "data": [
          {
            "from_parameter": "x"
          },
          {
            "from_parameter": "y"
          }
        ],
        "ignore_nodata": false
      },
      "result": true
    }
  }
}


PROCESS_DESCRIPTION_DICT["any"] = {
  "id": "any",
  "summary": "Is at least one value true?",
  "description": "Checks if **any** (i.e. at least one) value in `data` is `true`. If no value is given (i.e. the array is empty) the process returns `null`.\n\nBy default all no-data values are ignored so that the process returns `null` if all values are no-data, `true` if at least one value is true and `false` otherwise. Setting the `ignore_nodata` flag to `false` takes no-data values into account and the array values are reduced pairwise according to the following truth table:\n\n```\n      || null | false | true\n----- || ---- | ----- | ----\nnull  || null | null  | true\nfalse || null | false | true\ntrue  || true | true  | true\n```\n\n**Remark:** The process evaluates all values from the first to the last element and stops once the outcome is unambiguous. A result is ambiguous unless a value is `true`.",
  "categories": [
    "logic",
    "reducer"
  ],
  "parameters": [
    {
      "name": "data",
      "description": "A set of boolean values.",
      "schema": {
        "type": "array",
        "items": {
          "type": [
            "boolean",
            "null"
          ]
        }
      }
    },
    {
      "name": "ignore_nodata",
      "description": "Indicates whether no-data values are ignored or not and ignores them by default.",
      "schema": {
        "type": "boolean"
      },
      "default": true,
      "optional": true
    }
  ],
  "returns": {
    "description": "Boolean result of the logical operation.",
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
        "data": [
          false,
          null
        ]
      },
      "returns": false
    },
    {
      "arguments": {
        "data": [
          true,
          null
        ]
      },
      "returns": true
    },
    {
      "arguments": {
        "data": [
          false,
          null
        ],
        "ignore_nodata": false
      },
      "returns": null
    },
    {
      "arguments": {
        "data": [
          true,
          null
        ],
        "ignore_nodata": false
      },
      "returns": true
    },
    {
      "arguments": {
        "data": [
          true,
          false,
          true,
          false
        ]
      },
      "returns": true
    },
    {
      "arguments": {
        "data": [
          true,
          false
        ]
      },
      "returns": true
    },
    {
      "arguments": {
        "data": [
          false,
          false
        ]
      },
      "returns": false
    },
    {
      "arguments": {
        "data": [
          true
        ]
      },
      "returns": true
    },
    {
      "arguments": {
        "data": [
          null
        ],
        "ignore_nodata": false
      },
      "returns": null
    },
    {
      "arguments": {
        "data": []
      },
      "returns": null
    }
  ]
}


PROCESS_DESCRIPTION_DICT["not"] = {
  "id": "not",
  "summary": "Inverting a boolean",
  "description": "Inverts a single boolean so that `true` gets `false` and `false` gets `true`.\n\nThe no-data value `null` is passed through and therefore gets propagated.",
  "categories": [
    "logic"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "Boolean value to invert.",
      "schema": {
        "type": [
          "boolean",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "Inverted boolean value.",
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
        "x": null
      },
      "returns": null
    },
    {
      "arguments": {
        "x": false
      },
      "returns": true
    },
    {
      "arguments": {
        "x": true
      },
      "returns": false
    }
  ]
}


PROCESS_DESCRIPTION_DICT["or"] = {
  "id": "or",
  "summary": "Logical OR",
  "description": "Checks if **at least one** of the values is true. Evaluates parameter `x` before `y` and stops once the outcome is unambiguous. If a component is `null`, the result will be `null` if the outcome is ambiguous.\n\n**Truth table:**\n\n```\na \\ b || null | false | true\n----- || ---- | ----- | ----\nnull  || null | null  | true\nfalse || null | false | true\ntrue  || true | true  | true\n```",
  "categories": [
    "logic"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A boolean value.",
      "schema": {
        "type": [
          "boolean",
          "null"
        ]
      }
    },
    {
      "name": "y",
      "description": "A boolean value.",
      "schema": {
        "type": [
          "boolean",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "Boolean result of the logical OR.",
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
        "x": true,
        "y": true
      },
      "returns": true
    },
    {
      "arguments": {
        "x": false,
        "y": false
      },
      "returns": false
    },
    {
      "arguments": {
        "x": true,
        "y": null
      },
      "returns": true
    },
    {
      "arguments": {
        "x": null,
        "y": true
      },
      "returns": true
    },
    {
      "arguments": {
        "x": false,
        "y": null
      },
      "returns": null
    }
  ],
  "process_graph": {
    "any": {
      "process_id": "any",
      "arguments": {
        "data": [
          {
            "from_parameter": "x"
          },
          {
            "from_parameter": "y"
          }
        ],
        "ignore_nodata": false
      },
      "result": true
    }
  }
}


PROCESS_DESCRIPTION_DICT["xor"] = {
  "id": "xor",
  "summary": "Logical XOR (exclusive or)",
  "description": "Checks if **exactly one** of the values is true. If a component is `null`, the result will be `null` if the outcome is ambiguous.\n\n**Truth table:**\n\n```\na \\ b || null | false | true\n----- || ---- | ----- | -----\nnull  || null | null  | null\nfalse || null | false | true\ntrue  || null | true  | false\n```",
  "categories": [
    "logic"
  ],
  "parameters": [
    {
      "name": "x",
      "description": "A boolean value.",
      "schema": {
        "type": [
          "boolean",
          "null"
        ]
      }
    },
    {
      "name": "y",
      "description": "A boolean value.",
      "schema": {
        "type": [
          "boolean",
          "null"
        ]
      }
    }
  ],
  "returns": {
    "description": "Boolean result of the logical XOR.",
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
        "x": true,
        "y": true
      },
      "returns": false
    },
    {
      "arguments": {
        "x": false,
        "y": false
      },
      "returns": false
    },
    {
      "arguments": {
        "x": true,
        "y": false
      },
      "returns": true
    },
    {
      "arguments": {
        "x": true,
        "y": null
      },
      "returns": null
    },
    {
      "arguments": {
        "x": false,
        "y": null
      },
      "returns": null
    }
  ],
  "process_graph": {
    "not_x": {
      "process_id": "not",
      "arguments": {
        "x": {
          "from_parameter": "x"
        }
      }
    },
    "not_y": {
      "process_id": "not",
      "arguments": {
        "x": {
          "from_parameter": "y"
        }
      }
    },
    "and1": {
      "process_id": "and",
      "arguments": {
        "x": {
          "from_node": "not_x"
        },
        "y": {
          "from_parameter": "y"
        }
      }
    },
    "and2": {
      "process_id": "and",
      "arguments": {
        "x": {
          "from_parameter": "x"
        },
        "y": {
          "from_node": "not_y"
        }
      }
    },
    "or": {
      "process_id": "or",
      "arguments": {
        "x": {
          "from_node": "and1"
        },
        "y": {
          "from_node": "and2"
        }
      },
      "result": true
    }
  }
}
