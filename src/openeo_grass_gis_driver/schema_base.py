# -*- coding: utf-8 -*-
import json

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


class EoLinks(JsonableObject):
    """Additional links related to this collection.
    Could reference to other meta data formats
    with additional information or a preview image.

    rel:
        string

    href:
        required
        string <url>
        The value MUST be a dereferenceable URL.

    type:
        string
        The value MUST be a string that hints at the format used to
        represent data at the provided URI, preferably a mime-type.

    title:
        string
        Used as a human-readable label for a link.

    """

    def __init__(self, href: str, rel: str = None, type: str = None, title: str = None):
        self.str = href
        self.rel = rel
        self.type = type
        self.title = title

