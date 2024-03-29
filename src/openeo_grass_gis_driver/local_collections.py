# -*- coding: utf-8 -*-
import os
import json
from pathlib import Path
from openeo_grass_gis_driver.actinia_processing.base import (
    GrassDataType,
)
from openeo_grass_gis_driver.actinia_processing.config import Config


__license__ = "Apache License, Version 2.0"
__author__ = "Markus Metz"
__copyright__ = "Copyright 2018-2022, mundialis"
__maintainer__ = "mundialis"


def _create_collection_from_file(jsonfile):
    if not os.path.exists(jsonfile):
        return None

    with open(jsonfile) as f:
        collection = json.load(f)
        name = jsonfile.split("/")[-1][:-5]
        collection["id"] = f"local.eoarchive.{GrassDataType.EXTERN.value}.{name}"

    return collection


def get_local_collections():
    """Get local collections: read all local json files at configured
    path

    return: collections
    """

    # get list of all json files at given path
    local_collections_path = Config.LOCAL_COLLECTIONS
    local_collections_files = Path(local_collections_path).glob("**/*.json")
    jsonfiles = [str(f) for f in local_collections_files if f.is_file()]

    collections = {}
    collections["collections"] = []

    for j in jsonfiles:
        collection = _create_collection_from_file(j)
        collections["collections"].append(collection)

    return collections


def get_local_collection(name):
    """Get a local collection by name: read corresponding local
    json file at configured path

    return: collection
    """

    location, mapset, datatype, layer = name.split(".", 3)

    if location != "local":
        return None

    local_collections_path = Config.LOCAL_COLLECTIONS
    jsonfile = os.path.join(local_collections_path, "%s.json" % layer)
    collection = _create_collection_from_file(jsonfile)

    return collection
