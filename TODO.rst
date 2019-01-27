Version v0.3
============

Jobs
----

See https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Job-Management

Implement job management:

- job database interface to store and delete jobs                                   (partly done)
- job storage                                                                       (done)
- job information retrival                                                          (partly done)
- job running endpoint /jobs/<job_id>/result that triggers the batch job start
- job deletion                                                                      (partly done)
- Running job cancelling
- job cost estimation
- job information download

Process graphs
--------------

See https://open-eo.github.io/openeo-api/v/0.3.0/apireference/#tag/Process-Graph-Management

Implement process graph management endpoints:
- Storage endpoint
- Process graph validation              (done)
- Process graph preview                 (done)
- Full process graph info endpoint
- Process graph modification
- Process graph deletion
