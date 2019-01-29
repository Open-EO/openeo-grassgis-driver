# -*- coding: utf-8 -*-

from typing import Set, Dict, Optional, Tuple

# This is the process dictionary that is used to store all processes of the Actinia wrapper
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

class ProcessNode:
    """A single node in the process graph
    """

    def __init__(self, id, process_description: dict):

        self.id = id
        self.process: dict = process_description
        self.process_id: str = self.process["process_id"]
        self.arguments: Optional[dict] = None
        if "arguments" in self.process:
            self.arguments = self.process["arguments"]
        self.parents: Set[ProcessNode] = set()
        self.child: Optional[ProcessNode] = None

        self._process_description = process_description
        self._was_processed = False

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

        return f"Node: {self.id} parents: {parent_ids} child: {child_id}"

    def get_parent_ids(self) -> set:

        if not self.arguments:
            return set()

        parent_ids = set()

        for key in self.arguments:
            if isinstance(self.arguments[key], dict):
                if "from_node" in self.arguments[key]:
                    parent_ids.add(self.arguments[key]["from_node"])

        return parent_ids

    def asDict(self) -> dict:
        return self._process_description


class ProcessGraph:
    """This class represents a process graph

    """

    def __init__(self, graph_description: dict):
        """The constructor checks the validity of the provided dictionary
        and build the node interconnections

        :param graph_description:
        """

        if "title" not in graph_description:
            raise Exception("Title is required in the process graph")

        if "description" not in graph_description:
            raise Exception("Description is required in the process graph")

        if "process_graph" not in graph_description:
            raise Exception("process_graph is required in the process graph")

        self.title: str = graph_description["title"]
        self.description: str = graph_description["description"]
        self.node_dict: Dict[ProcessNode] = dict()
        self.root_nodes: Set[ProcessNode] = set()

        self.build_process_graph_from_description(graph_description=graph_description)

    def build_process_graph_from_description(self, graph_description: dict):
        """Build the directed process graph from the graph description

        :param graph_description: The description of the graph as dictionary
        :return: The set of child nodes that are the roots of the process graph
        """

        for key in graph_description["process_graph"].keys():
            process_description = graph_description["process_graph"][key]
            node = ProcessNode(id=key, process_description=process_description)
            self.node_dict[node.id] = node

        # Create node connections
        for node in self.node_dict.values():
            # Connect parents with childs
            parent_ids = node.get_parent_ids()
            if parent_ids:
                for parent_id in parent_ids:
                    parent_node = self.node_dict[parent_id]
                    node.parents.add(parent_node)
                    parent_node.child = node

        for node in self.node_dict.values():
            if node.child is None:
                self.root_nodes.add(node)


def process_node_to_actinia_process_chain(node: ProcessNode) -> Tuple[list, list]:
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
