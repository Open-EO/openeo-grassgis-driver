# -*- coding: utf-8 -*-
from pkg_resources import get_distribution, DistributionNotFound
# The location in which the job should be executed, that should only e a a single one
PROCESS_LOCATION = {}

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    __version__ = 'unknown'
