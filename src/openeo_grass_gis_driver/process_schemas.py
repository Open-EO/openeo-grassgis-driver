# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Tuple, Optional, Dict
from openeo_grass_gis_driver.schema_base import JsonableObject, EoLinks

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class DependentObject(JsonableObject):
    """This is the definition of a dependent object of a parameter

    description:
        string (description) Nullable
        Detailed description to fully explain the entity.

        CommonMark 0.28 syntax MAY be used for rich text representation.

    parameter:
        required
        string
        The name of the referenced parameter.

    ref_values:
        Array of any
        Embedded literal value that the referenced parameter MUST hold for this dependency to apply.
    """

    def __init__(self, parameter: str,
                 description: str,
                 ref_values: dict = None):

        self.parameter = parameter
        self.description = description
        self.ref_values = ref_values


class Parameter(JsonableObject):
    """This is a single parameter of a process

    description:
        required
        string (description) Nullable
        Detailed description to fully explain the entity.

        CommonMark 0.28 syntax MAY be used for rich text representation.

    required:
        boolean
        Default: false
        Determines whether this parameter is mandatory.

    deprecated:
        boolean
        Default: false
        Specifies that a parameter is deprecated and SHOULD be transitioned out of usage.

    mime_type:
        string
        The mime type that the parameter is formatted with.

    schema:
        required
        object (json_schema)
        A schema object according to the specification of JSON Schema draft-07.
        Additional values for format are defined centrally in the API documentation, e.g. bbox or crs.

    """

    def __init__(self, description: str,
                 schema: dict,
                 required: bool = False,
                 dependencies: Optional[List[DependentObject]] = None,
                 depricated: bool=False,
                 mime_type: Optional[str] = None):

        self.description = description
        self.schema = schema
        self.required = required
        self.dependencies = dependencies
        self.depricated = depricated
        self.mime_type = mime_type


class ReturnValue(JsonableObject):
    """
    description:
        required
        string (description) Nullable
        Detailed description to fully explain the entity.

        CommonMark 0.28 syntax MAY be used for rich text representation.

    mime_type:
        string
        The mime type that the returned data is formatted with.

    schema:
        required
        object (json_schema)
        A schema object according to the specification of JSON Schema draft-07.
        Additional values for format are defined centrally in the API documentation, e.g. bbox or crs.
    """

    def __init__(self, description: str, schema: dict, mime_type: Optional[str] = None):

        self.description = description
        self.schema = schema
        self.mime_type = mime_type


class ProcessException(JsonableObject):
    """
    code:
        integer
        Code to identify the exception.

    description:
        required
        string (description) Nullable
        Detailed description to fully explain the entity.

        CommonMark 0.28 syntax MAY be used for rich text representation.

    """

    def __init__(self, code: int,description: str):

        self.code = code
        self.description = description


class ProcessDescription(JsonableObject):

    def __init__(self, name: str, description: str,
                 parameters: Dict[str, Parameter],
                 returns: ReturnValue,
                 links: List[Optional[EoLinks]] = list(),
                 summary: Optional[str] = None,
                 min_parameters: Optional[int] = None,
                 deprecated: bool = False,
                 exceptions: Optional[Dict[str, ProcessException]] = None,
                 examples: Optional[Dict] = None):

        self.name = name
        self.description = description
        self.parameters = parameters
        self.returns = returns
        self.links = links
        self.summary = summary
        self.min_parameters = min_parameters
        self.deprecated = deprecated
        self.exceptions = exceptions
        self.examples = examples
