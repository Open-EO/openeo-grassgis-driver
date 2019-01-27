# -*- coding: utf-8 -*-
import json
from typing import List

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

    """

    def __init__(self, href: str, rel: str = None):
        self.str = href
        self.rel = rel

class EoLinks(JsonableObject):
    """Additional links related to this collection.
    Could reference to other meta data formats
    with additional information or a preview image.

    links: A list of EoLink's

    """

    def __init__(self, links: List[EoLink]):
        self.links = links

