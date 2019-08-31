# -*- coding: utf-8 -*-
import os

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class Config:
    # Settings for docker swarm image
    HOST="https://actinia.mundialis.de"
    PORT=443
    LOCATION="utm32n"
    # LOCATION="LL"
    LOCATIONS=["nc_spm_08", "latlong_wgs84", "utm32n"]
    USER="demouser"
    PASSWORD="gu3st!pa55w0rd"
    # The database file that stores the graphs
    GRAPH_DB="%s/.graph_db_file.sqlite"%os.environ["HOME"]
    # The database file that stores the jobs
    JOB_DB="%s/.job_db_file.sqlite"%os.environ["HOME"]
    # The database file that stores the actinia jobs
    ACTINIA_JOB_DB="%s/.actinia_job_db_file.sqlite"%os.environ["HOME"]
