# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from flask import make_response
import re
from typing import List, Tuple, Optional, Dict
from openeo_grass_gis_driver.schema_base import JsonableObject, EoLinks
from openeo_grass_gis_driver.process_graph_schemas import ProcessGraph
from openeo_grass_gis_driver.error_schemas import ErrorSchema

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class Parameter(JsonableObject):
    """This is a single parameter of a process

    description:
        required
        string (process_description) Nullable
        Detailed description to fully explain the entity.
        CommonMark 0.28 syntax MAY be used for rich text representation.

    required:
        boolean
        Default: false
        Determines whether this parameter is mandatory.

    deprecated:
        boolean
        Default: false
        Specifies that a parameter is deprecated and SHOULD be transitioned
        out of usage.

    experimental:
        boolean
        Default: false
        Specifies that a parameter is experimental and likely to change or
        produce unpredictable behaviour.

    media_type:
        string (process_media_type)
        The media (MIME) type that the value is encoded in.

    schema:
        required
        object (json_schema)
        A schema object according to the specification of JSON Schema draft-07.
        Additional values for format are defined centrally in the API
        documentation, e.g. bbox or crs.

    """

    def __init__(self, description: str,
                 schema: dict,
                 required: bool = False,
                 depricated: bool = False,
                 experimental: bool = False,
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
        string (process_description) Nullable
        Detailed description to fully explain the entity.
        CommonMark 0.28 syntax MAY be used for rich text representation.

    media_type:
        string (process_media_type)
        The media (MIME) type that the value is encoded in.

    schema:
        required
        object (json_schema)
        A schema object according to the specification of JSON Schema draft-07.
        Additional values for format are defined centrally in the API
        documentation, e.g. bbox or crs.
    """

    def __init__(self, description: str, schema: dict, media_type: Optional[str] = None):

        self.description = description
        self.schema = schema
        self.media_type = media_type


class ProcessException(JsonableObject):
    """
    description:
        string
        Detailed description to fully explain the error to client users
        and back-end developers.
        This should not be shown in the clients directly, but may be
        linked to in the errors url property.
        CommonMark 0.28 syntax MAY be used for rich text representation.

    message:
        required
        string
        Explains the reason the server is rejecting the request.
        This message is intended to be displayed to the client user.
        For "4xx" error codes the message should explain shortly how the
        client needs to modify the request.
        The message MAY contain variables, which are enclosed by curly
        brackets.
        Example: The value specified for the process argument '{argument}'
        in process '{process}' is invalid: {reason}

    http:
        integer
        Default: 400
        HTTP Status Code, following the error handling conventions in openEO.
        Defaults to 400.
    """

    def __init__(self, message: str, description: str, http: int = 400):

        self.message = message
        self.description = description
        self.http = http


class ProcessArguments(JsonableObject):
    # TODO please check if it is correct
    """
    Process Arguments

    (process_argument_value)
    """
    def __init__(self, arguments: List(ProcessArgumentValue) = None):
        self.arguments = arguments


class ProcessArgumentValue(JsonableObject):
    # TODO please check if it is correct
    """
    Process Argument Value (process_argument_value")
    Arguments for a process. See the API documentation for more information.

    one of:
        string
        number: "Number (incl. integers)"
        boolean
        object: Data that is expected to be passed from another process.
            from_node
                required
                string
                The ID of the node that data is expected to come from.
        object: Data that is expected to be passed to a callback from a calling process.
            from_argument
                required
                string
                The name of the parameter that is made available to a callback by a calling process
        object: Process graph to be executed as callback from withing the process.
            callback
                required
                (process_graph)
        array
            (process_argument_value")

    """

    def __init__(self, value):
        NumberTypes = (types.IntType, types.LongType, types.FloatType, types.ComplexType)
        if not (isinstance(value, list) and isinstance(value[0]), ProcessArgumentValue())
            and not isinstance(value, str) # string
            and not isinstance(value, (int, float, complex)) # number
            and not isinstance(value, bool) # boolean
            and (isinstance(value, object) and
            (not hasattr(value, 'from_node')
            and not hasattr(value, 'from_argument')
            and not hasattr(value, 'callback')):

            es = ErrorSchema(id=str(datetime.now()), code=400,
                message="A string, number, boolean, array of process argument values or an object with from_node, from_argument or callback attribute have to be set.")
            return make_response(es.to_json(), 400)
        self.value = value


class ProcessExample(JsonableObject):
    """
    Example, may be used for tests.
    # Either `process_graph` or `arguments` must be set, never both.

    title:
        string
        A title for the example.

    description:
        string (process_description)
        Detailed description to fully explain the entity.
        CommonMark 0.28 syntax MAY be used for rich text representation.
        In addition to the CommonMark syntax, clients can convert process IDs
        that are formatted as in the following example into links instead of
        code blocks: ``process_id()``

    process_graph:
        (process_graph)

    arguments:
        (process_arguments)

    returns: { }
    """

    def __init__(self, title: str = None, description: str = None,
        process_graph: ProcessGraph = None,
        arguments, # TODO
        returns):

        self.title = title
        self.description = description
        if (process_graph and arguments) or (not process_graph and not arguments):
            es = ErrorSchema(id=str(datetime.now()), code=400,
                message="Either process_graph or arguments must be set, never both.")
            return make_response(es.to_json(), 400)
        self.process_graph = process_graph
        self.arguments = arguments
        self.returns = returns


class ProcessDescription(JsonableObject):
    """

    id:
        required
        string (process_id) ^[A-Za-z0-9_]+$
        Unique identifier of the process.

    summary:
        string
        A short summary of what the process does.

    description:
        required
        string (process_description)
        Detailed description to fully explain the entity.
        CommonMark 0.28 syntax MAY be used for rich text representation.
        In addition to the CommonMark syntax, clients can convert process
        IDs that are formatted as in the following example into links
        instead of code blocks: ``process_id()``

    categories:
        Array of string
        A list of categories.

    parameter_order:
        Array of string
        Describes the order or the parameter for any environments that
        don't support named parameters. This property MUST be present
        for all processes with two or more parameters.
            Each item MUST correspond to a key in the `parameters` object.
            pattern: "^[A-Za-z0-9_]+$"

    parameters:
        required
        object
        A list of parameters that are applicable for this process.
        The keys of the object are the names of the parameters.
        They keys MUST match the following pattern: ^[A-Za-z0-9_]+$

    returns:
        required
        object
        The data that is returned from this process.

    deprecated:
        boolean
        Default: false
        Declares this process to be deprecated. Consumers SHOULD
        refrain from usage of the declared process.

    experimental:
        boolean
        Default: false
        Declares this process to be still experimental, which means
        that it is likely to change or produce unpredictable behaviour.

    exceptions:
        object
        Declares any exceptions (errors) that might occur during execution
        of this process. MUST be used only for exceptions that stop the
        execution of a process and are therefore not to be used for warnings,
        or notices or debugging messages. The keys define the error code
        and MUST match the following pattern: `^[A-Za-z0-9_]+$` This schema
        follows the schema of the general openEO error list (see errors.json).

    examples:
        Array of object
        Examples, may be used for tests. Either process_graph or arguments
        must be set, never both.

    links:
        Array of object (link)
        Related links, e.g. additional external documentation for this process.

    """

    def __init__(self, id: str, description: str,
                 parameters: Dict[str, Parameter],
                 returns: ReturnValue,
                 links: EoLinks = list(),
                 summary: Optional[str] = None,
                 # min_parameters: Optional[int] = None,
                 deprecated: bool = False,
                 experimental: bool = False,
                 exceptions: Optional[Dict[str, ProcessException]] = None,
                 examples: ProcessArguments = None,
                 categories: List[str] = None,
                 parameter_order: List[str] = None):

        # ID in pattern
        pattern = "^[A-Za-z0-9_]+$"
        x = re.search(pattern, id)
        if not x:
            es = ErrorSchema(id=str(datetime.now()), code=400,
                message="The process_id MUST match the following pattern: %s" % pattern)
            return make_response(es.to_json(), 400)
        self.id = id
        self.description = description
        # keys of parameters in pattern
        pattern = "^[A-Za-z0-9_]+$"
        for key in parameters:
            x = re.search(pattern, key)
            if not x:
                es = ErrorSchema(id=str(datetime.now()), code=400,
                    message="The keys of the parameters MUST match the following pattern: %s" % pattern)
                return make_response(es.to_json(), 400)
        self.parameters = parameters
        self.returns = returns
        self.links = links
        self.summary = summary
        # self.min_parameters = min_parameters
        self.deprecated = deprecated
        self.experimental = experimental
        self.exceptions = exceptions
        self.examples = examples
        self.categories = categories
        # parameter_order in pattern
        pattern = "^[A-Za-z0-9_]+$"
        if parameter_order:
            x = re.search(pattern, parameter_order)
            if not x:
                es = ErrorSchema(id=str(datetime.now()), code=400,
                    message="The parameter_order MUST match the following pattern: %s" % pattern)
                return make_response(es.to_json(), 400)
            self.parameter_order = parameter_order
