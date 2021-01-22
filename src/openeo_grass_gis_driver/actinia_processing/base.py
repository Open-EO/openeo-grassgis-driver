# -*- coding: utf-8 -*-
from enum import Enum
from typing import Set, Dict, Optional, Tuple, Union, List

# This is the process dictionary that is used to store all processes of the Actinia wrapper
from openeo_grass_gis_driver.actinia_processing.actinia_interface import ActiniaInterface

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph

ACTINIA_PROCESS_DESCRIPTION_DICT = {}
PROCESS_DESCRIPTION_DICT = {}
PROCESS_DICT = {}


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


###############################################################################
####### Version 0.4 of the API ################################################
###############################################################################


class GrassDataType(Enum):

    RASTER = "raster"
    VECTOR = "vector"
    STRDS = "strds"


class DataObject:
    """Data object that represents GRASS raster, vector and strds datatypes that can be defined in a process graph"""

    def __init__(self, name: str, datatype: GrassDataType, mapset: str = None, location: str = None):

        self.name = name
        self.datatype = datatype
        self.mapset = mapset
        self.location = location

    def __str__(self):
        return f"{self.location}.{self.mapset}.{self.datatype.value}.{self.name}"

    @staticmethod
    def from_string(name: str):

        location, mapset, datatype, layer_name = ActiniaInterface.layer_def_to_components(name)

        if datatype is None:
            raise Exception(f"Invalid collection id <{name}>")

        if GrassDataType.RASTER.value == datatype:
            return DataObject(name=layer_name, datatype=GrassDataType.RASTER, mapset=mapset, location=location)
        elif GrassDataType.VECTOR.value == datatype:
            return DataObject(name=layer_name, datatype=GrassDataType.VECTOR, mapset=mapset, location=location)
        elif GrassDataType.STRDS.value == datatype:
            return DataObject(name=layer_name, datatype=GrassDataType.STRDS, mapset=mapset, location=location)

        raise Exception(f"Unsupported object type <{datatype}>")

    def grass_name(self):

        if self.mapset:
            return f"{self.name}@{self.mapset}"
        return self.name

    def full_name(self):
        return str(self)

    def is_strds(self):

        return self.datatype == GrassDataType.STRDS

    def is_raster(self):

        return self.datatype == GrassDataType.RASTER

    def is_vector(self):

        return self.datatype == GrassDataType.VECTOR


class Node:
    """A single node in the process graph
    """

    def __init__(self, id, process_description: dict):

        self.id = id
        self.process: dict = process_description
        self.process_id: str = self.process["process_id"]
        self.arguments: Optional[dict] = None
        if "arguments" in self.process:
            self.arguments = self.process["arguments"]
        self.parents: Set[Node] = set()
        self.parents_dict: Dict[str, Node] = dict()
        self.children: Set[Node] = set()
        self._process_description = process_description
        self._was_processed = False
        self.output_objects: Set[DataObject] = set()

    def add_output(self, output_object: DataObject):
        self.output_objects.add(output_object)

    def get_parent_by_name(self, parent_name: str) -> Optional['Node']:
        if parent_name in self.parents_dict.keys():
            return self.parents_dict[parent_name]
        return None

    @property
    def processed(self):
        return self._was_processed

    @processed.setter
    def processed(self, flag: bool):
        self._was_processed = flag

    def __str__(self):

        child_ids = list()
        if self.children:
            child_ids = [node.id for node in self.children]

        parent_ids = list()
        if self.parents:
            parent_ids = [node.id for node in self.parents]

        parent_names = list()
        if self.parents_dict:
            parent_names = list(self.parents_dict.keys())

        return f"Node: {self.id} parent names: {parent_names} parent ids: {parent_ids} child ids: {child_ids}"

    def get_parents_dict(self) -> dict:

        if not self.arguments:
            return dict()

        parent_dict = dict()

        for key in self.arguments:
            if isinstance(self.arguments[key], dict):
                if "from_node" in self.arguments[key]:
                    parent_dict[key] = self.arguments[key]["from_node"]

        return parent_dict

    def as_dict(self) -> dict:
        return self._process_description


class Graph:
    """This class represents a process graph

    """

    def __init__(self, graph_description: Union[Dict, ProcessGraph]):
        """The constructor checks the validity of the provided dictionary
        and build the node interconnections

        :param graph_description:
        """

        self.node_dict: Dict[str, Node] = dict()
        self.root_nodes: Set[Node] = set()
        if isinstance(graph_description, ProcessGraph):
            self.title: str = graph_description.title
            self.description: str = graph_description.description
            self.build_process_graph_from_description(process_graph=graph_description.process_graph)
        else:
            if "title" not in graph_description:
                # raise Exception("Title is required in the process graph")
                graph_description["title"] = "synchronous processing"

            if "description" not in graph_description:
                # raise Exception("Description is required in the process graph")
                graph_description["description"] = "generated by using direct execution endpoint"

            # graph_description can be a process with process_graph or
            # only a process_graph
            if "process" not in graph_description and \
               "process_graph" not in graph_description:
                raise Exception("process_graph is required in the process graph")

            if "process" in graph_description and \
               "process_graph" not in graph_description["process"]:
                raise Exception("process_graph is required in the process")

            if "process" in graph_description:
                process_graph = graph_description["process"]["process_graph"]
            else:
                process_graph = graph_description["process_graph"]
            self.title: str = graph_description["title"]
            self.description: str = graph_description["description"]

            self.build_process_graph_from_description(process_graph=process_graph)

    def build_process_graph_from_description(self, process_graph: dict):
        """Build the directed process graph from the graph description

        :param graph_description: The description of the graph as dictionary
        :return: The set of child nodes that are the roots of the process graph
        """

        if "process_graph" in process_graph:
            process_graph = process_graph["process_graph"]

        for key in process_graph.keys():
            process_description = process_graph[key]
            node = Node(id=key, process_description=process_description)
            self.node_dict[node.id] = node

        # Create node connections
        for node in self.node_dict.values():
            # Connect parents with childs
            parent_dict = node.get_parents_dict()
            if parent_dict:
                for parent_name in parent_dict.keys():
                    parent_node = self.node_dict[parent_dict[parent_name]]
                    node.parents.add(parent_node)
                    node.parents_dict[parent_name] = parent_node
                    parent_node.children.add(node)

        for node in self.node_dict.values():
            if len(node.children) == 0:
                self.root_nodes.add(node)

    def to_actinia_process_list(self) -> Tuple[list, list]:
        """Compute the actinia process list traversing the tree from all root nodes"""

        full_process_list = list()
        full_output_object_list = list()

        for node in self.root_nodes:
            output_object_list, process_list = process_node_to_actinia_process_chain(node=node)
            full_process_list.extend(process_list)
            full_output_object_list.extend(output_object_list)

        return full_output_object_list, full_process_list


def process_node_to_actinia_process_chain(node: Node) -> Tuple[list, list]:
    """This function calls the openEO process node to actinia process chain converter process
    based on the node process_id.

    It will gather the actinia process chain and the output identifier of the
    process converter and sets the node status to processed==True.

    :param node: A single process node
    :return: (output_oblect_list, process_list)
    """

    if node is None:
        raise Exception("Missing process node")

    process_list = []
    output_object_list = []

    if node.process_id not in PROCESS_DICT:
        raise Exception("Unsupported process id, available processes: %s" % PROCESS_DICT.keys())

    outputs, processes = PROCESS_DICT[node.process_id](node)
    process_list.extend(processes)
    output_object_list.extend(outputs)

    node.processed = True

    return output_object_list, process_list


def check_node_parents(node: Node) -> Tuple[list, list]:
    process_list = []
    input_objects = []

    for parent in node.parents:
        i, p = process_node_to_actinia_process_chain(parent)
        process_list.extend(p)
        input_objects.extend(i)

    return input_objects, process_list
