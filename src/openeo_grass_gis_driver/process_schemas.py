# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Tuple, Optional, Dict
from openeo_grass_gis_driver.schema_base import JsonableObject, EoLinks

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


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

    experimental:
        boolean
        Default: false

        Specifies that a parameter is experimental and likely to change or produce unpredictable behaviour.

    media_type:
        string
        The media (MIME) type that the value is encoded in.

    schema:
        required
        object (json_schema)
        A schema object according to the specification of JSON Schema draft-07.
        Additional values for format are defined centrally in the API documentation, e.g. bbox or crs.

    """

    def __init__(self, description: str,
                 schema: dict,
                 required: bool = False,
                 depricated: bool=False,
                 experimental: bool=False,
                 mime_type: Optional[str] = None):

        self.description = description
        self.schema = schema
        self.required = required
        self.depricated = depricated
        self.experimental = experimental
        self.mime_type = mime_type


class ReturnValue(JsonableObject):
    """
    description:
        required
        string (description) Nullable
        Detailed description to fully explain the entity.

        CommonMark 0.28 syntax MAY be used for rich text representation.

    media_type:
        string
        The media (MIME) type that the value is encoded in.

    schema:
        required
        object (json_schema)
        A schema object according to the specification of JSON Schema draft-07.
        Additional values for format are defined centrally in the API documentation, e.g. bbox or crs.
    """

    def __init__(self, description: str, schema: dict, media_type: Optional[str] = None):

        self.description = description
        self.schema = schema
        self.media_type = media_type


class ProcessException(JsonableObject):
    """
    description:
        string
        Detailed description to fully explain the error to client users and back-end developers.
        This should not be shown in the clients directly, but may be linked to in the errors url property.

        CommonMark 0.28 syntax MAY be used for rich text representation.

    message:
        required
        string
        Explains the reason the server is rejecting the request. This message is intended to be displayed to the
        client user. For "4xx" error codes the message should explain shortly how the client needs to modify the request.
        The message MAY contain variables, which are enclosed by curly brackets. Example: {variable_name}

    http:
        integer
        Default: 400

        HTTP Status Code, following the error handling conventions in openEO. Defaults to 400.


    """

    def __init__(self, message: str, description: str, http: int = 400):

        self.message = message
        self.description = description
        self.http = http


class ProcessDescription(JsonableObject):
    """
    id:

        string (process_id) ^[A-Za-z0-9_]+$

    required:

        Unique identifier of the process.

    summary:
        string

        A short summary of what the process does.

    description:
        required

        string (process_description)

        Detailed description to fully explain the entity.

        CommonMark 0.28 syntax MAY be used for rich text representation. In addition to the CommonMark syntax, clients can convert process IDs that are formatted as in the following example into links instead of code blocks: ``process_id()``

    categories:
        Array of string

        A list of categories.

    parameter_order:
        Array of string

        Describes the order or the parameter for any environments that don't support named parameters. This property MUST be present for all processes with two or more parameters.

    parameters:
        required

        object

        A list of parameters that are applicable for this process. The keys of the object are the names of the parameters. They keys MUST match the following pattern: ^[A-Za-z0-9_]+$

    returns:
        required

        object

        The data that is returned from this process.

    deprecated:
        boolean
        Default: false

        Declares this process to be deprecated. Consumers SHOULD refrain from usage of the declared process.

    experimental:
        boolean
        Default: false

        Declares this process to be still experimental, which means that it is likely to change or produce unpredictable behaviour.

    exceptions:
        object

        Declares any exceptions (errors) that might occur during execution of this process. MUST be used only for exceptions that stop the execution of a process and are therefore not to be used for warnings, or notices or debugging messages.

        The keys define the error code and MUST match the following pattern: ^[A-Za-z0-9_]+$

        This schema follows the schema of the general openEO error list (see errors.json).

    examples:
        Array of object

        Examples, may be used for tests. Either process_graph or arguments must be set, never both.

    links:
        Array of object (link)

        Related links, e.g. additional external documentation for this process.

    """

    def __init__(self, id: str, description: str,
                 parameters: Dict[str, Parameter],
                 returns: ReturnValue,
                 links: EoLinks = list(),
                 summary: Optional[str] = None,
                 min_parameters: Optional[int] = None,
                 deprecated: bool = False,
                 exceptions: Optional[Dict[str, ProcessException]] = None,
                 examples: Optional[Dict] = None):

        self.id = id
        self.description = description
        self.parameters = parameters
        self.returns = returns
        self.links = links
        self.summary = summary
        self.min_parameters = min_parameters
        self.deprecated = deprecated
        self.exceptions = exceptions
        self.examples = examples
