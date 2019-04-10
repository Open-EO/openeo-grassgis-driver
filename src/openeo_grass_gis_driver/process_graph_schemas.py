# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Tuple, Optional, Dict
from openeo_grass_gis_driver.schema_base import JsonableObject, EoLinks, EoLink
from openeo_grass_gis_driver.process_schemas import ProcessArguments

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ProcessGraphNode(JsonableObject):
    """This is the definition of a single process graph

    process_id:
        required
        string (process_id) ^[A-Za-z0-9_]+$
        Unique identifier of the process.

    result:
        boolean
        Used to specify which node is the last in the chain and returns
        the result to return to the requesting context. This flag MUST
        only be set once in each list of process nodes.
        default: false

    description:
        string (description)
        Detailed description to fully explain the entity.
        CommonMark 0.28 syntax MAY be used for rich text representation.

    arguments:
        required
        ProcessArguments (process_arguments)
}
    """

    def __init__(self, process_id: str, description: str = None,
        arguments: ProcessArguments, result: bool = False):

        # ID in pattern
        pattern = "^[A-Za-z0-9_]+$"
        x = re.search(pattern, id)
        if not x:
            es = ErrorSchema(id=str(datetime.now()), code=400,
                message="The process_id MUST match the following pattern: %s" % pattern)
            return make_response(es.to_json(), 400)
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
