# -*- coding: utf-8 -*-
from openeo_grass_gis_driver.actinia_processing.config import Config \
    as ActiniaConfig
from openeo_grass_gis_driver.actinia_processing.base import \
    ACTINIA_PROCESS_DESCRIPTION_DICT, \
    ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.actinia_processing.actinia_interface import \
    ActiniaInterface


__license__ = "Apache License, Version 2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021 mundialis"
__maintainer__ = "mundialis"


def register_processes():

    iface = ActiniaInterface()
    iface.set_auth(ActiniaConfig.USER, ActiniaConfig.PASSWORD)
    # TODO: add logger
    print("Requesting modules from actinia...")
    status_code, modules = iface.list_modules()

    if status_code == 200:
        # TODO: add logger
        print("Registering modules...")
        for module in modules:
            # convert grass module names to openeo process names
            process = module["id"].replace('.', '_')
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
            ACTINIA_PROCESS_DESCRIPTION_DICT[process] = module

            # create "pseudo" modules which comply to openeo
            if ('returns' in module and
                    type(module['returns']) is list and
                    len(module['returns']) > 0):
                # create "pseudo" module for every output:
                for returns in module['returns']:
                    pm = dict(module)
                    pm['returns'] = returns
                    process = "%s_%s" % (
                        pm['id'].replace('.', '_'), returns['name'])
                    ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT[process] = pm

            else:
                # if no output, assign empty object
                module['returns'] = {}
                ACTINIA_OPENEO_PROCESS_DESCRIPTION_DICT[process] = module

        # TODO: add logger
        print("... successfully registered modules!")
