# -*- coding: utf-8 -*-
from flask import json
import unittest
from datetime import datetime
from pprint import pprint
from openeo_grass_gis_driver.collection_schemas import Extent, CollectionEntry, Collection, EoLinks
from openeo_grass_gis_driver.collection_schemas import CollectionInformation
from openeo_grass_gis_driver.test_base import TestBase

__license__ = "Apache License, Version 2.0"
__author__ = "Sören Gebbert"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Soeren Gebbert"
__email__ = "soerengebbert@googlemail.com"


class ResponseSchemaTestCase(TestBase):

    def test_collection_entry(self):

        cl = EoLinks(href="http://unknown", rel="unknown", type="unknown", title="unknown")
        print("CollectionLinks", cl.to_json())

        e = Extent(spatial=(10,20,30,40), temporal=(str(datetime(2000,1,1)), None))
        print("Extent", e.to_json())

        ce = CollectionEntry(name="raster", description="Test", title="title", license="unknown",
                             extent=e, links=[cl,])
        print("CollectionEntry", ce.to_json())

        c = Collection(collections=[ce,], links=[cl,])
        print("Collection", c.to_json())

        ci = CollectionInformation(name="raster", description="Test", title="title", license="unknown",
                             extent=e, links=[cl,])
        print("CollectionInformation", ci.to_json())


if __name__ == "__main__":
    unittest.main()
