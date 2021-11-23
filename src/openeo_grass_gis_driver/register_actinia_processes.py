# -*- coding: utf-8 -*-
from openeo_grass_gis_driver.actinia_processing.config import Config \
    as ActiniaConfig
from openeo_grass_gis_driver.actinia_processing.base import \
    ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT, \
    OPENEO_ACTINIA_ID_DICT, \
    T_BASENAME_MODULES_LIST
from openeo_grass_gis_driver.actinia_processing.actinia_interface import \
    ActiniaInterface
from openeo_grass_gis_driver.utils.logging import log


__license__ = "Apache License, Version 2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021 mundialis"
__maintainer__ = "mundialis"


def register_processes():

    iface = ActiniaInterface()
    iface.set_auth(ActiniaConfig.USER, ActiniaConfig.PASSWORD)
    log.info("Requesting modules from %s..." % ActiniaConfig.HOST)
    status_code, modules = iface.list_modules()

    if status_code == 200:
        for module in modules:
            # convert grass module names to openeo process names
            # special treatment for GRASS modules in
            # T_BASENAME_MODULES_LIST
            if module["id"] in T_BASENAME_MODULES_LIST:
                if "parameters" in module:
                    module["parameters"] = [
                        i for i in module["parameters"] if i["name"] != "basename"
                    ]
                if "returns" in module:
                    module["returns"] = [
                        i for i in module["returns"] if i["name"] != "basename"
                    ]
            process = module["id"].replace('.', '_')
            actiniaid = module["id"]
            if "parameters" in module:
                for item in module["parameters"]:
                    if "subtype" in item["schema"]:
                        if item["schema"]["subtype"] in ("cell", "strds"):
                            item["schema"]["type"] = "object"
                            item["schema"]["subtype"] = "raster-cube"
            if "returns" in module:
                for item in module["returns"]:
                    if "subtype" in item["schema"]:
                        if item["schema"]["subtype"] in ("cell", "strds"):
                            item["schema"]["type"] = "object"
                            item["schema"]["subtype"] = "raster-cube"

            # create "pseudo" modules which comply to openeo
            if ('returns' in module and
                    type(module['returns']) is list and
                    len(module['returns']) > 0):
                # create "pseudo" module for every output:
                for returns in module['returns']:
                    pm = dict(module)
                    pm["links"] = dict()
                    pm["links"]["about"] = (
                        "https://grass.osgeo.org/grass80/manuals/%s.html" % pm["id"]
                    )
                    pm['returns'] = returns
                    process = "%s_%s" % (
                        pm['id'].replace('.', '_'), returns['name'])
                    pm['id'] = process
                    ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT[process] = pm
                    OPENEO_ACTINIA_ID_DICT[process] = {
                        "id": actiniaid,
                        "returns": returns["name"]
                    }
            else:
                # if no output, assign empty object
                module["links"] = dict()
                module["links"]["about"] = (
                    "https://grass.osgeo.org/grass80/manuals/%s.html" % module["id"]
                )
                module['returns'] = {}
                module["id"] = process
                OPENEO_ACTINIA_ID_DICT[process] = {"id": actiniaid}
                ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT[process] = module

        log.info("... successfully registered modules!")

    else:
        log.error('... error registering modules!')
