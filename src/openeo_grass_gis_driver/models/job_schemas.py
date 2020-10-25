# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from datetime import datetime
from typing import List, Optional, Dict

from openeo_grass_gis_driver.models.error_schemas import ErrorSchema
from openeo_grass_gis_driver.models.schema_base import JsonableObject, EoLinks
from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"



class Argument(JsonableObject):
    """	Describes a general argument for various entities.

    description:
        required
        string
        A brief description of the argument.

    required:
        boolean
        Determines whether this argument is mandatory.
        default: false

    default:
        any
        The default value represents what would be assumed by the consumer
        of the input as the value of the argument if none is provided.
        The value MUST conform to the defined type for the argument defined
        at the same level. For example, if type is string, then default can
        be "foo" but cannot be 1.

    minimum:
        number
        Minimum value allowed for numeric arguments.

    maximum:
        number
        Maximum value allowed for numeric arguments.

    enum:
        array of any
        List of allowed values for this argument. To represent examples that
        cannot be naturally represented in JSON, a string value can be used
        to contain the example with escaping where necessary.
            items: A single value allowed for this argument.

    example:
        any
        A free-form property to include an example for this argument.
        To represent examples that cannot be naturally represented in JSON,
        a string value can be used to contain the example with escaping
        where necessary.

"""
    def __init__(self, description: str, minimum: Optional[int] = None,
                 maximum: Optional[int] = None, required: bool = False,
                 default = None, enum: List = None, example = None):

        self.description = description
        self.required = required
        self.default = default
        #if not isinstance(minimum, (int, float, complex)):
        #    es = ErrorSchema(id=str(datetime.now().isoformat()), code=400,
        #        message="The minimum MUST be a number")
        #self.minimum = minimum
        #if not isinstance(maximum, (int, float, complex)):
        #    es = ErrorSchema(id=str(datetime.now().isoformat()), code=400,
        #        message="The maximum MUST be a number")
        self.minimum = minimum
        self.maximum = maximum
        self.enum = enum
        self.example = example


class OutputFormat(JsonableObject):
    """Describes a specific output format. The key of the entry is
    the output format name.
    https://open-eo.github.io/openeo-api/#operation/list-file-types

    gis_data_types:
        required
        Array of string
        Items Enum:"raster" "vector" "table" "other"
        Specifies the supported GIS spatial data type for this format.

    parameters:
        object (Output Format Parameters)
        Specifies the supported parameters for this output format.

    links:
        Array of object (Link)
        Additional links related to this output format, e.g. more
        information about the parameters.

    """

    def __init__(self, gis_data_types: List[str],
            links: List[Optional[EoLinks]] = None,
            parameters: List[Argument] = None):

        self.gis_data_types = gis_data_types
        self.links = links
        self.parameters = parameters


class JobError(JsonableObject):
    """This is the error response schema
    An error message that describes the problem during the batch job
    execution. May only be available if the `status` is `error`.
    The error MUST be cleared if the job is started again (i.e. the
    status changes to `queue`).

    code:
        required
        string (error_code)
        The code is either one of the standardized error codes or a
        custom error code.

    message:
        required
        string (error_message)
        A message explaining what the client may need to change or what
        difficulties the server is facing. By default the message must
        be sent in English language. Content Negotiation is used to localize
        the error messages: If an Accept-Language header is sent by the
        client and a translation is available, the message should be
        translated accordingly and the Content-Language header must be
        present in the response.
        example: "A sample error message.

    id:
        string (error_id)
        A back-end may add a unique identifier to the error response to be
        able to log and track errors with further non-disclosable details.
        A client could communicate this id to a back-end provider to get
        further information.
        example: "550e8400-e29b-11d4-a716-446655440000"

    links:
        array of links (error_links)
        Additional links related to this error, e.g. a resource that is
        explaining the error and potential solutions in-depth or a contact
        e-mail address.
    """

    def __init__(self, code: int, message: str,
                 links: List[Optional[EoLinks]] = list(), id: str = None):

        # Standardized status codes:
        # https://open-eo.github.io/openeo-api/#section/API-Principles/Error-Handling
        standardized_status_codes = {
            200: "OK",
            201: "Created",
            202: "Accepted",
            204: "No Content",
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden",
            404: "Not Found",
            500: "Internal Server Error",
            501: "Not Implemented"}
        self.id = id
        self.code = standardized_status_codes[code]
        self.message = message
        self.links = links


class JobInformation(JsonableObject):
    """Information about a job
    https://open-eo.github.io/openeo-api/#operation/describe-job

    id:
        required
        string r"^[A-Za-z0-9_\-\.~]+$" (job_id)
        Unique identifier of a job that is generated by the back-end during
        job submission. MUST match the specified pattern.

    title:
        string
        A short description to easily distinguish entities.

    description:
        string
        Detailed description to fully explain the entity.
        CommonMark 0.28 syntax MAY be used for rich text representation.

    status:
        required
        string
        The current status of a batch job.
        Default: "submitted"
        Enum:"submitted" "queued" "running" "canceled" "finished" "error"

    created:
        required (created)
        string <date-time>
        Date and time of creation, formatted as a RFC 3339 date-time.

    updated:
        string <date-time> (updated)
        Date and time of last status change, formatted as a RFC 3339 date-time.

    plan:
        string (billing_plan)
        The billing plan to process and charge the job with. The plans can
        be retrieved by calling GET /. Billing plans MUST be accepted
        case insensitive.

    costs:
        number (money)
        An amount of money or credits. The value MUST be specified in
        the currency the back-end is working with. The currency can be
        retrieved by calling GET /.

    budget:
        number (budget) Nullable
        Default: null
        Maximum amount of costs the user is allowed to produce. The value
        MUST be specified in the currency the back-end is working with.
        The currency can be retrieved by calling GET /. If possible, back-ends
        SHOULD reject jobs with openEO error PaymentRequired if the budget is
        too low to process the request completely. Otherwise, when reaching
        the budget jobs MAY try to return partial results if possible.
        Otherwise the request and results are discarded. Users SHOULD be
        warned by clients that reaching the budget MAY discard the results
        and that setting this value should be well-wrought. Setting the buget
        to null means there is no specified budget.
    """

    def __init__(self, id: str, created: str,
                 process: ProcessGraph, title: str = None,
                 description: str = None, status: str = "created",
                 updated: Optional[str] = None,
                 plan: str = None, cost: float = None, budget: float = None):
        # Test id
        #pattern = "^[A-Za-z0-9_\-\.~]+$"
        #x = re.search(pattern, job_id)
        #if not x:
        #    es = ErrorSchema(id=str(datetime.now().isoformat()), code=400,
        #        message="The id MUST match the following pattern: %s" % pattern)
        #    return make_response(es.to_json(), 400)
        self.id = id
        self.title = title
        self.description = description
        # Test Status
        #if status in ["submitted", "queued", "running", "canceled", "finished", "error"]:
        #    es = ErrorSchema(id=str(datetime.now().isoformat()), code=400,
        #        message="The status has to one of \"submitted\" \"queued\" \"running\" \"canceled\" \"finished\" \"error\"")
        #    return make_response(es.to_json(), 400)
        self.status = status
        self.created = created
        self.updated = updated
        self.plan = plan
        self.cost = cost
        self.budget = budget
        self.process = process
        self.links = None


class JobList(JsonableObject):
    """A collection of job description entries

    https://open-eo.github.io/openeo-api/#operation/list-jobs
    """

    def __init__(self, jobs: List[JobInformation],
                 links: Optional[EoLinks] = None):
        self.jobs = jobs
        self.links = links
