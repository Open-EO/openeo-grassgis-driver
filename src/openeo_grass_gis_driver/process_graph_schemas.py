# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Tuple, Optional, Dict
from openeo_grass_gis_driver.schema_base import JsonableObject, EoLinks, EoLink

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessGraphNode(JsonableObject):
    """This is the definition of a single process graph

    """

    def __init__(self, process_id: str, description: str, arguments: dict(), result: bool = False):

        self.process_id = process_id
        self.description = description
        self.arguments = arguments
        self.result = result


class ProcessGraph(JsonableObject):
    """This is the definition of a process graph with title and description

    """

    def __init__(self, title: str, description: str, process_graph: Dict[str, ProcessGraphNode]):

        self.title = title
        self.description = description
        self.process_graph = process_graph


class ProcessGraphListEntry(JsonableObject):
    """An entry in the process graph list

    """

    def __init__(self, title: str, description: str, id: str):

        self.title = title
        self.description = description
        self.id = id


class ProcessGraphList(JsonableObject):
    """A list of process graph definitions

    """

    def __init__(self, process_graphs: List[ProcessGraphListEntry],
                 links: Optional[EoLinks] = None):

        self.process_graphs = process_graphs
        self.links = links
