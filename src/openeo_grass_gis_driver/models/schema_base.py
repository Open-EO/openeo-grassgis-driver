# -*- coding: utf-8 -*-
import json
from typing import List, Optional

from flask import make_response

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


def as_dict_without_nones(o):

    d = o.__dict__

    r = dict()

    for key in d:
        if d[key] is None:
            continue
        # allow nullable but required keys
        value = d[key]
        if value == "json:null":
            value = None
        elif  value == "json:true":
            value = True
        elif  value == "json:false":
            value = False
        # ___ is a placeholder for : as in eo:bands
        r[key.replace("___", ":")] = value

    return r


class JsonableObject:
    """This class is the base class for all openEO responses that serialises
    the response classes into JSON"""

    def to_json(self):
        return json.dumps(self, default=lambda o: as_dict_without_nones(o), sort_keys=False, indent=2)

    def as_response(self, http_status):
        response = make_response(self.to_json(), http_status)
        response.headers['Content-Type'] = 'application/json'
        return response


class Link(JsonableObject):
    """A link to another resource on the web. Bases on RFC5899 and SHOULD
    follow registered link relation types whenever feasible.

    rel:
        string

    href:
        required
        string <url>
        The value MUST be a dereferenceable URL.

    type:
        string
        The value MUST be a string that hints at the format used to represent
        data at the provided URI, preferably a media (MIME) type.

    title:
        string
        Used as a human-readable label for a link.

    """

    def __init__(self, href: str, title: Optional[str] = None,
            rel: Optional[str] = None, type_: Optional[str] = None):
        self.href = href
        self.title = title
        self.rel = rel
        self.type = type_


class EoLink(JsonableObject):
    """link related to this collection.

    rel:
        string

    href:
        required
        string <url>
        The value MUST be a dereferenceable URL.

    type:
        string

        The value MUST be a string that hints at the format used to represent data at
        the provided URI, preferably a media (MIME) type.

    title:
        string

        Used as a human-readable label for a link.

    """

    def __init__(self, href: str, title: Optional[str] = None,
            rel: Optional[str] = None, type_: Optional[str] = None):
        self.href = href
        self.title = title
        self.rel = rel
        self.type = type_


class EoLinks(JsonableObject):
    """Additional links related to this collection.
    Could reference to other meta data formats
    with additional information or a preview image.

    links: A list of EoLink's

    """

    def __init__(self, links: List[EoLink]):
        self.links = links


class UDFLinks(JsonableObject):
    """Related links, e.g. additional external documentation for this runtime.

    array of (link)

    """

    def __init__(self, links: List[Link]):
        self.links = links


class ListLinks(JsonableObject):
    """Additional links related to this list of resources.
    Could reference to alternative formats such as a
    rendered HTML version. The links could also be used for
    pagination using the [rel types]
    (https://www.iana.org/assignments/link-relations/link-relations.xhtml)
    `first`, `prev`, `next` and `last`. Pagination is
    currently OPTIONAL and clients may not support it.
    Therefore it MUST be implemented in a way that clients
    not supporting pagination get all resources regardless.

    links: A list of EoLink's

    """

    def __init__(self, links: List[EoLink]):
        self.links = links

class File(JsonableObject):
    """ Workspace File
    path:
        string
        Path of the file, relative to the user's root directory. MUST NOT
        start with a slash and MUST NOT be url-encoded.
        example: "folder/file.txt"

    size:
        integer
        File size in bytes.
        example: 1024

    modified:
        string (date-time)
        Date and time the file has lastly been modified, formatted as
        a RFC 3339 date-time.
        example: "2018-01-03T10:55:29Z"

    """

    def __init__(self, path: str = None, size: int = None, modified: str = None):
        self.path = path
        self.size = size
        self.modified = modified
