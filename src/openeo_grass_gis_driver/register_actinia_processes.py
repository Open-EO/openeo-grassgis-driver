# -*- coding: utf-8 -*-
from openeo_grass_gis_driver.actinia_processing.config import Config \
    as ActiniaConfig
from openeo_grass_gis_driver.actinia_processing.base import \
    ACTINIA_PROCESS_DESCRIPTION_DICT
from openeo_grass_gis_driver.actinia_processing.actinia_interface import \
    ActiniaInterface


__license__ = "Apache License, Version 2.0"
__author__ = "Carmen Tawalika"
__copyright__ = "Copyright 2021 mundialis"
__maintainer__ = "mundialis"


def register_processes():

    iface = ActiniaInterface()
    iface.set_auth(ActiniaConfig.USER, ActiniaConfig.PASSWORD)
    status_code, modules = iface.list_modules()

    if status_code == 200:
        for module in modules:
            # TODO: add logger
            # print("registering %s" % module['id'])
            ACTINIA_PROCESS_DESCRIPTION_DICT[module['id']] = module

    # overwrite certain module to collect more information
    status_code, module = iface.list_module('r.slope.aspect')
    if status_code == 200:
        ACTINIA_PROCESS_DESCRIPTION_DICT[module['id']] = module
