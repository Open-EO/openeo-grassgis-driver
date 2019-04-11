# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Tuple, Optional, Dict
from openeo_grass_gis_driver.models.schema_base import JsonableObject, EoLinks

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ErrorSchema(JsonableObject):
    """This is the error response schema
    An error object declares addtional information about a client-side
    or server-side error. The openEO documentation
    (https://open-eo.github.io/openeo-api/v/0.4.0/errors/index.html)
    provides additional information regarding error handling and a
    list of potential error codes.

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

        # Standardized status codes: https://open-eo.github.io/openeo-api/v/0.4.0/errors/index.html
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
