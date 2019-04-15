# -*- coding: utf-8 -*-

from typing import Set, Dict, Optional, Tuple, Union

# This is the process dictionary that is used to store all processes of the Actinia wrapper
from openeo_grass_gis_driver.process_graph_schemas import ProcessGraph

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
        self.child: Optional[Node] = None
        self._process_description = process_description
        self._was_processed = False
        self.output_names = set()

    def add_output(self, output_name: str):
        self.output_names.add(output_name)

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

        child_id = None
        if self.child is not None:
            child_id = self.child.id

        parent_ids = list()
        if self.parents:
            parent_ids = [node.id for node in self.parents]

        parent_names = list()
        if self.parents_dict:
            parent_names = list(self.parents_dict.keys())

        return f"Node: {self.id} parent names: {parent_names} parent ids: {parent_ids} child: {child_id}"

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
                raise Exception("Title is required in the process graph")

            if "description" not in graph_description:
                raise Exception("Description is required in the process graph")

            if "process_graph" not in graph_description:
                raise Exception("process_graph is required in the process graph")

            self.title: str = graph_description["title"]
            self.description: str = graph_description["description"]

            self.build_process_graph_from_description(process_graph=graph_description["process_graph"])

    def build_process_graph_from_description(self, process_graph: dict):
        """Build the directed process graph from the graph description

        :param graph_description: The description of the graph as dictionary
        :return: The set of child nodes that are the roots of the process graph
        """

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
                    parent_node.child = node

        for node in self.node_dict.values():
            if node.child is None:
                self.root_nodes.add(node)


def process_node_to_actinia_process_chain(node: Node) -> Tuple[list, list]:
    """This function calls the openEO process node to actinia process chain converter process
    based on the node process_id.

    It will gather the actinia process chain and the output identifier of the
    process converter and sets the node status to processed==True.

    :param node: A single process node
    :return: (output_name_list, process_list)
    """

    if node is None:
        raise Exception("Missing process node")

    process_list = []
    output_name_list = []

    if node.process_id not in PROCESS_DICT:
        raise Exception("Unsupported process id, available processes: %s" % PROCESS_DICT.keys())

    outputs, processes = PROCESS_DICT[node.process_id](node)
    process_list.extend(processes)
    output_name_list.extend(outputs)

    node.processed = True

    return output_name_list, process_list


def check_node_parents(node: Node) -> Tuple[list, list]:
    process_list = []
    input_names = []

    for parent in node.parents:
        i, p = process_node_to_actinia_process_chain(parent)
        process_list.extend(p)
        input_names.extend(i)

    return input_names, process_list