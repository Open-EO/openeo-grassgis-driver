# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Optional, Dict
from .schema_base import JsonableObject, EoLinks

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class OutputFormat(JsonableObject):
    """Information about the output format

    https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Job-Management/paths/~1jobs~1{job_id}/get
    """

    def __init__(self, format: str, parameters: Dict[str, str]):

        self.format = format
        self.parameters = parameters


class JobInformation(JsonableObject):
    """Information about a job

    https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Job-Management/paths/~1jobs~1{job_id}/get
    """

    def __init__(self, job_id: str, title: str,
                 description: str, status: str,
                 process_graph: dict(),
                 output: Optional[OutputFormat],
                 submitted: str, updated: Optional[str],
                 plan: str = "free", cost: float= 0.0, budget: float = 0.0,
                 links: Optional[EoLinks] = None):
        self.job_id = job_id
        self.title = title
        self.description = description
        self.process_graph = process_graph
        self.output = output
        self.status = status
        self.submitted = submitted
        self.updated = updated
        self.plan =plan
        self.cost = cost
        self.budget = budget
        self.additional_info = None
        self.links = links



class JobList(JsonableObject):
    """A collection of job description entries

    https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Job-Management/paths/~1jobs/get
    """

    def __init__(self, jobs: List[JobInformation],
                 links: Optional[EoLinks] = None):
        self.jobs = jobs
        self.links = links
