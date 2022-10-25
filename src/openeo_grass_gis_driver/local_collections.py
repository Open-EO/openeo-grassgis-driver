# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path

from openeo_grass_gis_driver.actinia_processing.actinia_interface import (
    ActiniaInterface,
)
from openeo_grass_gis_driver.actinia_processing.config import Config


__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018-2021, mundialis"
__maintainer__ = "mundialis"


def get_local_collections():
    """Get local collections: read all local json files at configured
    path

    return: collections
    """

    # get list of all json files at given path
    local_collections_path = Config.LOCAL_COLLECTIONS
    jsonfiles = [
        str(f) for f in Path(local_collections_path).glob("**/*.json") if f.is_file()
    ]

    collections = {}
    collections["collections"] = []

    for j in jsonfiles:
        with open(j) as f:
            collection = json.load(f)
            name = j.split("/")[-1][:-5]
            collection["id"] = "local.mapset.gdallocal.%s" % name
            collections["collections"].append(collection)

    return collections


def get_local_collection(name):
    """Get a local collection by name: read all local json files at configured
    path

    return: collection
    """

    iface = ActiniaInterface()
    location, mapset, datatype, layer = iface.layer_def_to_components(name)

    if location != "local":
        return None

    local_collections_path = Config.LOCAL_COLLECTIONS
    jsonfile = os.path.join(local_collections_path, "%s.json" % layer)

    if not os.path.exists(jsonfile):
        return None

    with open(jsonfile) as f:
        collection = json.load(f)
        name = jsonfile.split("/")[-1][:-5]
        collection["id"] = "local.mapset.gdallocal.%s" % name

    return collection
