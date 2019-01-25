# -*- coding: utf-8 -*-

# This is the process dictionary that is used to store all processes of the Actinia wrapper
PROCESS_DESCRIPTION_DICT = {}
PROCESS_DICT = {}


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


# TODO: Rewrite this function to reflect the process graph approach that allows branches
def analyse_process_graph(graph):
    """Analyse a process graph and call the required subprocess analysis

    This function return the list of input names for the next process and the
    Actinia process chain that was build before.

    :param graph: The process description
    :return: (output_name_list, process_list)
    """

    if graph is None:
        raise Exception("Empty process graph")

    process_list = []
    output_name_list = []

    for key in graph:
        process = graph[key]

        if "process_id" in process:

            if process["process_id"] not in PROCESS_DICT:
                raise Exception("Unsupported process id, available processes: %s"%PROCESS_DICT.keys())

            outputs, processes = PROCESS_DICT[process["process_id"]](process)
            process_list.extend(processes)
            output_name_list.extend(outputs)

    return output_name_list, process_list


class ProcessNode:
    """A single node in the process graph
    """

    def __init__(self, id, process_description: dict):

        self.id = id
        print("id", self.id)
        self.process = process_description
        self.process_id = self.process["process_id"]
        self.arguments = None
        if "arguments" in self.process:
            self.arguments = self.process ["arguments"]
        self.parents = set()
        self.child = None

        self._process_description = process_description

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

    def __init__(self, graph_description: dict):

        if "title" not in graph_description:
            raise Exception("Title is required in the process graph")

        if "description" not in graph_description:
            raise Exception("Description is required in the process graph")

        if "process_graph" not in graph_description:
            raise Exception("process_graph is required in the process graph")

        self.title = graph_description["title"]
        self.description = graph_description["description"]
        self.root_nodes = self.build_process_graph_from_description(graph_description=graph_description)

    @staticmethod
    def build_process_graph_from_description(graph_description: dict) -> set:
        """Build the directed process graph from the graph description

        :param graph_description: The description of the graph as dictionary
        :return: The set of child nodes that are the roots of the process graph
        """

        node_dict = dict()
        root_nodes = set()

        if "process_graph" in graph_description:
            for key in graph_description["process_graph"].keys():
                process_description = graph_description["process_graph"][key]
                node = ProcessNode(id=key, process_description=process_description)
                node_dict[node.id] = node

        # Create node connections
        for node in node_dict.values():
            # Connect parents with childs
            parent_ids = node.get_parent_ids()
            if parent_ids:
                for parent_id in parent_ids:
                    parent_node = node_dict[parent_id]
                    node.parents.add(parent_node)
                    parent_node.child = node

        for node in node_dict.values():
            if node.child is None:
                root_nodes.add(node)

        return root_nodes
