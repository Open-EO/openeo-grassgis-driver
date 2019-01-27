# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Tuple, Optional, Dict
from .schema_base import JsonableObject, EoLinks
from datetime import datetime

__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class JobInformation(JsonableObject):
    """Information about a job
    """

    def __init__(self, job_id: str, title: str,
                 description: str, status: str,
                 submitted: datetime, updated: datetime,
                 plan: str = "free", cost: float= 0.0, budget: float = 0.0):
        self.job_id = job_id
        self.title = title
        self.description = description
        self.status = status
        self.submitted = submitted
        self.updated = updated
        self.plan =plan
        self.cost = cost
        self.budget = budget


class JobList(JsonableObject):
    """A collection of job description entries
    """

    def __init__(self, jobs: List[JobInformation],
                 links: List[Optional[EoLinks]] = EoLinks(href="unknown")):
        self.jobs = jobs
        self.links = links
