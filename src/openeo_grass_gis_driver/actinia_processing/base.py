# -*- coding: utf-8 -*-
from enum import Enum
from typing import Set, Dict, Optional, Tuple, Union
from random import randint
import uuid

# This is the process dictionary that is used to store all processes of
# the Actinia wrapper
from openeo_grass_gis_driver.actinia_processing.actinia_interface import \
     ActiniaInterface

from openeo_grass_gis_driver.models.process_graph_schemas import ProcessGraph

# actinia process descriptions converted to openeo API:
# pseudo modules, one for each output,
# if actinia modules can produce several outputs
ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT = {}
# mapping of openeo process ids to actinia process ids
OPENEO_ACTINIA_ID_DICT = {}
# list of t.* GRASS modules needing special treatment because of a
# basename option (basename for new raster maps) required together with
# the name of the output strds
T_BASENAME_MODULES_LIST = [
    "t.rast3d.algebra",
    "t.rast3d.extract",
    "t.rast3d.mapcalc",
    "t.rast.accdetect",
    "t.rast.accumulate",
    "t.rast.aggregate.ds",
    "t.rast.aggregate",
    "t.rast.algebra",
    "t.rast.bandcalc",
    "t.rast.contour",
    "t.rast.extract",
    "t.rast.gapfill",
    "t.rast.import",
    "t.rast.mapcalc",
    "t.rast.neighbors",
    "t.rast.ndvi",
    "t.rast.resample",
    "t.rast.to.vect",
]
# standard openeo process descriptions
PROCESS_DESCRIPTION_DICT = {}
PROCESS_DICT = {}


__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "mundialis"


###############################################################################
# Version 0.4 of the API ################################################
###############################################################################


class GrassDataType(Enum):

    RASTER = "raster"
    VECTOR = "vector"
    STRDS = "strds"


class DataObject:
    """Data object that represents GRASS raster, vector and strds datatypes
    that can be defined in a process graph
    """

    def __init__(
            self,
            name: str,
            datatype: GrassDataType,
            mapset: str = None,
            location: str = None):

        self.name = name
        self.datatype = datatype
        self.mapset = mapset
        self.location = location

    def __str__(self):
        re = f"{self.location}.{self.mapset}.{self.datatype.value}.{self.name}"
        return re

    @staticmethod
    def from_string(name: str):

        AI = ActiniaInterface
        location, mapset, datatype, layer_name = AI.layer_def_to_components(
            name)

        if datatype is None:
            raise Exception(f"Invalid collection id <{name}>")

        if GrassDataType.RASTER.value == datatype:
            return DataObject(
                name=layer_name,
                datatype=GrassDataType.RASTER,
                mapset=mapset,
                location=location)
        elif GrassDataType.VECTOR.value == datatype:
            return DataObject(
                name=layer_name,
                datatype=GrassDataType.VECTOR,
                mapset=mapset,
                location=location)
        elif GrassDataType.STRDS.value == datatype:
            return DataObject(
                name=layer_name,
                datatype=GrassDataType.STRDS,
                mapset=mapset,
                location=location)

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

        return (f"Node: {self.id} parent names: {parent_names} parent "
                f"ids: {parent_ids} child ids: {child_ids}")

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
            self.build_process_graph_from_description(
                process_graph=graph_description.process_graph)
        else:
            if "title" not in graph_description:
                # raise Exception("Title is required in the process graph")
                graph_description["title"] = "synchronous processing"

            if "description" not in graph_description:
                # raise Exception("Description is required in process graph")
                descr = "generated by using direct execution endpoint"
                graph_description["description"] = descr

            # graph_description can be a process with process_graph or
            # only a process_graph
            if "process" not in graph_description and \
               "process_graph" not in graph_description:
                raise Exception(
                    "process_graph is required in the process graph")

            if "process" in graph_description and \
               "process_graph" not in graph_description["process"]:
                raise Exception("process_graph is required in the process")

            if "process" in graph_description:
                process_graph = graph_description["process"]["process_graph"]
            else:
                process_graph = graph_description["process_graph"]
            self.title: str = graph_description["title"]
            self.description: str = graph_description["description"]

            self.build_process_graph_from_description(
                process_graph=process_graph)

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
        """Compute the actinia process list traversing the tree from all root
        nodes
        """

        full_process_list = list()
        full_output_object_list = list()

        for node in self.root_nodes:
            pn2pc = process_node_to_actinia_process_chain
            output_object_list, process_list = pn2pc(node=node)
            full_process_list.extend(process_list)
            full_output_object_list.extend(output_object_list)

        return full_output_object_list, full_process_list


def process_node_to_actinia_process_chain(node: Node) -> Tuple[list, list]:
    """This function calls the openEO process node to actinia process chain
    converter process based on the node process_id.

    It will gather the actinia process chain and the output identifier of the
    process converter and sets the node status to processed==True.

    :param node: A single process node
    :return: (output_oblect_list, process_list)
    """

    if node is None:
        raise Exception("Missing process node")

    process_list = []
    output_object_list = []

    if node.processed is True:
        return output_object_list, process_list

    if node.process_id in PROCESS_DICT:
        outputs, processes = PROCESS_DICT[node.process_id](node)
    elif node.process_id in ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT:
        # native actinia process
        outputs, processes = openeo_to_actinia(node)
    else:
        raise Exception("Unsupported process id '%s'" % node.process_id)

    process_list.extend(processes)
    output_object_list.extend(outputs)

    node.processed = True

    return output_object_list, process_list


def openeo_to_actinia(node: Node) -> Tuple[list, list]:
    """Generic translator of openeo to actinia for actinia modules that
       have been translated to openeo processes with
       register_processes()

    :param node: The process node
    :return: (output_objects, actinia_process_list)
    """
    input_objects, process_list = check_node_parents(node=node)

    output_objects = []

    # openeo process name and GRASS module name
    process_name = node.process_id
    # get module name as returned by actinia
    module_name = OPENEO_ACTINIA_ID_DICT[process_name]["id"]
    openeo_returns = None
    if "returns" in OPENEO_ACTINIA_ID_DICT[process_name]:
        openeo_returns = OPENEO_ACTINIA_ID_DICT[process_name]["returns"]

    # get module description from actinia
    # to find out which parameters are input and which are output
    # -> output is in the returns block if existing
    iface = ActiniaInterface()
    status_code, module = iface.list_module(module_name)
    if status_code != 200:
        raise Exception("Unsupported actinia process '%s'" % module_name)

    rn = randint(0, 1000000)

    actinia_id = "%s_%i" % (process_name, rn)

    # create an actinia process chain entry of the form

    #    pc = {"id": "t_rast_mapcalc_%i" % rn,
    #          "module": "t.rast.mapcalc",
    #          "inputs": [{"param": name,
    #                      "value": answer},
    #                     {"param": name,
    #                      "value": answer},
    #                      ...
    #                    ],
    #           "flags": ...
    #          }

    # from openeo

    # "process_id": module_name,
    #    "arguments": {
    #        key: value,
    #        key: value,
    #        ...
    #    }

    pc = {}
    pc["id"] = actinia_id
    pc["module"] = module_name
    pc["inputs"] = []
    pc["flags"] = None

    # input parameters
    data_object = None
    for key in node.arguments.keys():
        # is key a valid actinia option ?
        ao = None
        # not very elegant
        for item in module["parameters"]:
            if item["name"] == key:
                ao = item
        if ao is None:
            # warning, error, exception?
            continue
        # check if it is an input object
        if isinstance(node.arguments[key], dict) and \
           "from_node" in node.arguments[key]:
            # input option comes from another node in the process graph
            # which output object in the set of output_objects?
            value = list(
                node.get_parent_by_name(
                    parent_name=key).output_objects)[0]
            data_object = value
            # check schema subtype of parameter and compare with
            # datatype of data_object
            if ao["schema"]["subtype"] == "cell" and \
                    data_object.datatype != GrassDataType.RASTER:
                raise Exception(
                    "Wrong input data type, expecting 'cell'")
            elif ao["schema"]["subtype"] == "strds" and \
                    data_object.datatype != GrassDataType.STRDS:
                raise Exception(
                    "Wrong input data type, expecting 'strds'")
            elif ao["schema"]["subtype"] == "vector" and \
                    data_object.datatype != GrassDataType.VECTOR:
                raise Exception(
                    "Wrong input data type, expecting 'vector'")

            param = {"param": key,
                     "value": data_object.grass_name()}
            pc["inputs"].append(param)
        elif ao["schema"]["type"] == "boolean":
            # flag
            if node.arguments[key] is True:
                if pc["flags"] is None:
                    pc["flags"] = key
                else:
                    pc["flags"] = pc["flags"] + key
        else:
            # option answer, treat as string
            value = node.arguments[key]
            param = {"param": key,
                     "value": str(value)}
            pc["inputs"].append(param)

    if pc["flags"] is None:
        del pc["flags"]

    # TODO: support modules that do not have input maps
    if data_object is None:
        raise Exception(
            "No input data object for actinia process '%s'" %
            module_name)

    # output parameters
    if "returns" in module and openeo_returns is not None:
        # find openeo_returns in "returns" of the
        # actinia module description
        key = openeo_returns
        for item in module["returns"]:
            # not very elegant
            ao = None
            if item["name"] == key:
                ao = item
            if ao is None:
                continue
            datatype = None
            if ao["schema"]["subtype"] == "cell":
                datatype = GrassDataType.RASTER
            elif ao["schema"]["subtype"] == "vector":
                datatype = GrassDataType.VECTOR
            elif ao["schema"]["subtype"] == "strds":
                datatype = GrassDataType.STRDS

            if datatype is not None:
                # note that key is already added to the process name
                # in order to distinguish between different outputs
                # of the same module
                output_object = DataObject(
                    name=create_output_name(data_object.name, process_name),
                    datatype=datatype)
                param = {"param": key,
                         "value": output_object.grass_name()}
                pc["inputs"].append(param)
                output_objects.append(output_object)
                node.add_output(output_object=output_object)
        if module_name in T_BASENAME_MODULES_LIST:
            param = {"param": "basename",
                     "value": output_object.grass_name()}
            pc["inputs"].append(param)

    process_list.append(pc)

    return output_objects, process_list


def check_node_parents(node: Node) -> Tuple[list, list]:
    process_list = []
    input_objects = []

    for parent in node.parents:
        i, p = process_node_to_actinia_process_chain(parent)
        process_list.extend(p)
        input_objects.extend(i)

    return input_objects, process_list


def create_output_name(input: str, process_name: str):
    new_uuid = uuid.uuid4().hex

    # names must start with a letter
    if input.find("uuid") == 0 and "_" in input:
        insuffix = input.split("_", 1)[1]
        output = f"uuid{new_uuid}_{insuffix}_{process_name}"
    else:
        output = f"uuid{new_uuid}_{input}_{process_name}"

    return output
