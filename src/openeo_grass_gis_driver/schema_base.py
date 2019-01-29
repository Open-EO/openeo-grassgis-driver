# -*- coding: utf-8 -*-
import json
from typing import List, Optional

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
        r[key] = d[key]

    return r


class JsonableObject:
    """This class is the base class for all openEO responses that serialises
    the response classes into JSON"""

    def to_json(self):
        return json.dumps(self, default=lambda o: as_dict_without_nones(o), sort_keys=False, indent=2)


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

    def __init__(self, href: str, title: Optional[str] = None, rel: Optional[str] = None, type_: Optional[str] = None):
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

