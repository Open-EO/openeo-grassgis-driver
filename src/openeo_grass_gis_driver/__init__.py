# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound
# The location in which the job should be executed, that should only e a a
# single one
PROCESS_LOCATION = {}

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"
