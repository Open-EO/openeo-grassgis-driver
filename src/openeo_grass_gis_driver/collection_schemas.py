# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Tuple, Optional
from .schema_base import JsonableObject, EoLinks

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class Extent(JsonableObject):
    """
    spatial:
        Array of number
        The potential spatial extent covered by the collection.
        The bounding box is provided as four or six numbers, depending on whether
        the coordinate reference system includes a vertical axis (height or depth):

        West (lower left corner, coordinate axis 1)
        South (lower left corner, coordinate axis 2)
        Base (optional, lower left corner, coordinate axis 3)
        East (upper right corner, coordinate axis 1)
        North (upper right corner, coordinate axis 2)
        Height (optional, upper right corner, coordinate axis 3)
        The coordinate reference system of the values is WGS84 longitude/latitude.

    temporal:
        Array of string <date-time>
        Potential temporal extent covered by the collection.
        The temporal extent specified by a start and an end time,
        each formatted as a RFC 3339 date-time. Open date ranges are
        supported and can be specified by setting one of the times to null.
        Setting both entries to null is not allowed. Only the Gregorian calendar is supported.

    """

    def __init__(self, spatial: Optional[Tuple[float, float, float, float]] = None,
                 temporal: Optional[Tuple[str, Optional[str]]] = None):
        self.spatial = spatial
        self.temporal = temporal


class CollectionEntry(JsonableObject):
    """
    name:
        required
        string (collection_name) ^[A-Za-z0-9_\-\.~\/]+$
        Unique identifier for EO collections. MUST match the specified pattern.

    title:
        string (collection_title)
        A short descriptive one-line title for the collection.

    description:
        required
        string (collection_description)
        Detailed multi-line description to fully explain the collection.
        CommonMark 0.28 syntax MAY be used for rich text representation.

    license:
        required
        string (license)
        Collection's license(s) as a SPDX License identifier, SPDX expression,
        or the string proprietary if the license is not on the SPDX license list.
        Proprietary licensed data SHOULD add a link to the license text with the l
        icense relation in the links section (not as a value of this fields).

        """

    def __init__(self, name: str, title=None, description: str = None, license: str = None,
                 links: List[Optional[EoLinks]] = list(), extent: Extent = Extent()):
        self.name = name
        self.title = title
        self.description = description
        self.license = license
        self.extent = extent
        self.links = links


class Collection(JsonableObject):
    """A collection of data description entries
    """

    def __init__(self, collections: List[CollectionEntry],
                 links: List[Optional[EoLinks]] = EoLinks(href="unknown")):
        self.collections = collections
        self.links = links


class CollectionInformation(CollectionEntry):

    def __init__(self, keywords: Optional[List[str]] = None, version: str = None, **kwargs):
        super(CollectionInformation, self).__init__(**kwargs)

        self.keywords = keywords
        self.version = version



