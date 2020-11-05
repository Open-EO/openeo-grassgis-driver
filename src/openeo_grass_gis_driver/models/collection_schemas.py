# -*- coding: utf-8 -*-
"""This file includes all required openEO response schemas
"""
from typing import List, Tuple, Optional
from flask import make_response
import re
from datetime import datetime
from openeo_grass_gis_driver.models.schema_base import JsonableObject, EoLinks, EoLink
from openeo_grass_gis_driver.models.error_schemas import ErrorSchema

__author__ = "Sören Gebbert, Anika Bettge"
__copyright__ = "Copyright 2018, Sören Gebbert, mundialis"
__maintainer__ = "Sören Gebbert"
__email__ = "soerengebbert@googlemail.com"


class CollectionExtent(JsonableObject):
    """
    (collection_extent)
    spatial:
        required
        Array of array of number
        The potential spatial extent covered by the collection.
        The bounding box is provided as four or six numbers, depending on whether
        the coordinate reference system includes a vertical axis (height or depth):

        West (lower left corner, coordinate axis 1)
        South (lower left corner, coordinate axis 2)
        Base (optional, lower left corner, coordinate axis 3)
        East (upper right corner, coordinate axis 1)
        North (upper right corner, coordinate axis 2)
        Height (optional, upper right corner, coordinate axis 3)
        The coordinate reference system of the values is WGS84 longitude/latitude.

    temporal:
        required
        Array of array of string <date-time>
        Potential temporal extent covered by the collection.
        The temporal extent specified by a start and an end time,
        each formatted as a RFC 3339 date-time. Open date ranges are
        supported and can be specified by setting one of the times to null.
        Setting both entries to null is not allowed. Only the Gregorian calendar is supported.

    """

    def __init__(self,
                 spatial: Tuple[float, float, float, float] = (-180, -90, 180, 90),
                 temporal: Optional[Tuple[str, Optional[str]]] = ("1900-01-01T00:00:00", "2100-01-01T00:00:00")):

        # This is soooo stupid, why is the temporal extent required? There is data that has no temporal extent
        # So we trick here to set an arbitrary extent of 200 years
        
        # list of bboxes !
        bbox = []
        bbox.append(spatial)    # TODO maxItems: 6
        self.spatial = {"bbox": bbox}
        # list of intervals !
        interval = []
        interval.append(temporal)
        self.temporal = {"interval": interval}

class CollectionProperties(JsonableObject):
    """
    (collection_properties)
    
    currently only STAC EO (electro-optical)
    missing: STAC other extensions, STAC SAR, STAC Scientific
             see https://open-eo.github.io/openeo-api/#operation/describe-collection

    eo:gsd
        required
        number
        The nominal Ground Sample Distance for the data, as measured in
        meters on the ground. Since GSD can vary across a scene
        depending on projection, this should be the average or most
        commonly used GSD in the center of the image. If the data
        includes multiple bands with different GSD values, this should
        be the value for the greatest number or most common bands. For
        instance, Landsat optical and short-wave IR bands are all 30
        meters, but the panchromatic band is 15 meters. The eo:gsd
        should be 30 meters in this case since those are the bands most
        commonly used.
    
    eo:platform
        required
        string
        Unique name of the specific platform the instrument is attached
        to. For satellites this would be the name of the satellite
        (e.g., landsat-8, sentinel-2A), whereas for drones this would
        be a unique name for the drone.

    eo:constellation
        string
        The name of the group of satellites that have similar payloads
        and have their orbits arranged in a way to increase the
        temporal resolution of acquisitions of data with similar
        geometric and radiometric characteristics. Examples are the
        Sentinel-2 constellation, which has S2A and S2B and RapidEye.
        This field allows users to search for Sentinel-2 data, for
        example, without needing to specify which specific platform the
        data came from.

    eo:instrument
        required
        string
        The name of the sensor used, although for Items which contain
        data from multiple sensors this could also name multiple
        sensors. For example, data from the Landsat-8 platform is
        collected with the OLI sensor as well as the TIRS sensor, but
        the data is distributed together and commonly referred to as
        OLI_TIRS.

    eo:epsg
        number <epsg-code> Nullable
        EPSG code of the datasource, null if no EPSG code.
        A Coordinate Reference System (CRS) is the native reference
        system (sometimes called a 'projection') used by the data, and
        can usually be referenced using an EPSG code. If the data does
        not have a CRS, such as in the case of non-rectified imagery
        with Ground Control Points, eo:epsg should be set to null. It
        should also be set to null if a CRS exists, but for which there
        is no valid EPSG code.

    eo:bands
        required
        Array of objects (STAC EO Band)
        This is a list of the available bands where each item is a Band
        Object.
    """

    def __init__(
            self, eo_gsd: float = None, eo_platform: str = None,
            eo_constellation: str = None, eo_instrument: str = None,
            eo_epsg: int = None, eo_bands = None):
        self.eo___gsd = eo_gsd
        self.eo___platform = eo_platform
        self.eo___constellation = eo_constellation
        self.eo___instrument = eo_instrument
        self.eo___epsg = eo_epsg
        self.eo___bands = eo_bands



class EOBands(JsonableObject):
    """
    name:
        string
        The name of the band (e.g., "B01", "B02", "B1", "B5", "QA").

    common_name:
        string
        Not required, but STRONGLY RECOMMENDED! The name commonly used to refer
        to the band to make it easier to search for bands across instruments.
        See the "Common Band Names" for a list of accepted common names.

    description:
        strings
        nullable: true
        $ref: "#/components/schemas/description"

    gsd:
        number
        Ground Sample distance, the nominal distance between pixel centers
        available, in meters. See eo:gsd for more information. Defaults to
        eo:gsd if not provided.

    accuracy:
        number
        The expected error between the measured location and the true location
        of a pixel, in meters on the ground.

    center_wavelength:
        number
        The center wavelength of the band, in micrometers (μm).

    full_width_half_max:
        number
        Full width at half maximum (FWHM) is a common way to describe the size
        of a spectral band. It is the width, in micrometers (μm), of the
        bandpass measured at a half of the maximum transmission. Thus, if the
        maximum transmission of the bandpass was 80%, the FWHM is measured as
        the width of the bandpass at 40% transmission.

    offset
        number
        default: 0
        Offset to convert band values to the actual measurement scale.

    scale:
        number
        default: 1
        Scale to convert band values to the actual measurement scale.

    unit:
        string (url-format)
        The unit of measurement for the data, specified as OGC URN.

    nodata:
        array of numbers
        Specific values representing no data.

    periodicity:
        string
        Periodictity of the measurements, preferably specified using ISO 8601.
    """

    def __init__(
            self, name: str = None, common_name: str = None, gsd: float = None,
            accuracy: float = None, center_wavelength: float = None,
            full_width_half_max: float = None, offset: float = 0,
            unit: str = None, nodata: List[int] = None, periodicity: str = None,
            scale: int = 1, description: Optional[str] = None):
        self.name = name
        self.common_name = common_name
        self.description = description
        self.gsd = gsd
        self.accuracy = accuracy
        self.center_wavelength = center_wavelength
        self.full_width_half_max = full_width_half_max
        self.offset = offset
        self.scale = scale
        self.unit = unit
        self.nodata = nodata
        self.periodicity = periodicity


class SarBands(JsonableObject):
    """
    name:
        string
        The name of the band.

    common_name:
        Description to fully explain the band, should include processing
        information. CommonMark 0.28 syntax MAY be used for rich textrepresentation.

    data_type:
        string
        Specifies the type of the data contained in the band, for example
        `amplitude`, `intensity`, `phase`, `angle`, `sigma0`, `gamma0`.

    unit:
        string (url-format)
        The unit of measurement for the data, specified as OGC URN.

    polarization:
        string
        nullable: true
        The polarization of the band, either `HH`, `VV`, `HV`, `VH` or `null`
        if not applicable.
        "HH", "VV", "HV", "VH", null
    """

    def __init__(
            self, name: str = None, common_name: str = None,
            data_type: str = None, unit: str = None, polarization: str = None):

        self.name = name
        self.common_name = common_name
        self.data_type = data_type
        self.unit = unit
        self.polarization = polarization


# class CollectionSar(JsonableObject): TODO Doppelpunkte
#     """
#     STAC Scientific
#
#     sar:platform:
#         required
#         string
#         Unique name of the specific platform the instrument is attached to. For
#         satellites this would be the name of the satellite (e.g., landsat-8,
#         sentinel-2A), whereas for drones this would be a unique name for the
#         drone.
#
#     sci:doi:
#         string
#         The DOI name of the collection, e.g. `10.1000/xyz123`.
#         This MUST NOT be a DOIs link. For all DOI names
#         respective DOI links SHOULD be added to the links
#         section of the collection with relation type `cite-as`.
#         pattern: "^(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![%"#? ])\S)+)$"
#
#     sci:citation:
#         string
#         The recommended human-readable reference (citation) to
#         be used by publications citing this collection. No
#         specific citation style is suggested, but the citation
#         should contain all information required to find the
#         publication distinctively.
#
#     sci:publications:
#         List of SciPublications
#         A list of publications which describe and reference the collection.
#     """


# class SciPublications(JsonableObject): # only used for CollectionSar
#     """
#     STAC Scientific Publications
#     A list of publications which describe and reference the collection.
#
#     doi:
#         string
#         The DOI name of a publication which describes and references
#         the collection. The publications should include more information
#         about the collection and how it was processed. This MUST NOT be
#         a DOIs link. For all DOI names respective DOI links SHOULD be
#         added to the links section of the collection with relation type
#         `cite-as`.
#         pattern: "^(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![%"#? ])\S)+)$"
#
#     citation:
#         string
#         Human-readable reference (citation) of a publication which
#         describes and references the collection. The publications
#         should include more information about the collection and how
#         it was processed. No specific citation style is suggested,
#         but a citation should contain all information required to
#         find the publication distinctively.
#
#     """
#     def __init__(self, doi: str = None, citation: str = None):
#
#        pattern = "^(10[.][0-9]{4,}(?:[.][0-9]+)*/(?:(?![%"#? ])\S)+)$"
#        x = re.search(pattern, doi)
#        if not x:
#            es = ErrorSchema(id=str(datetime.now().isoformat()), code=400,
#                message="The doi MUST match the following pattern: %s" % pattern)
#            return make_response(es.to_json(), 400)
#         self.doi = doi
#         self.citation = citation


# class CollectionSar(JsonableObject): TODO Doppelpunkte
#     """
#     sar:platform:
#         required
#         string
#         Unique name of the specific platform the instrument is attached to. For
#         satellites this would be the name of the satellite (e.g., landsat-8,
#         sentinel-2A), whereas for drones this would be a unique name for the
#         drone.
#
#     sar:constellation:
#         string
#         sar:constellation is the name of the group of satellites that have
#         similar payloads and have their orbits arranged in a way to increase
#         the temporal resolution of acquisitions of data with similar geometric
#         and radiometric characteristics. Examples are the Sentinel-1
#         constellation, which has S1A, S1B, S1C and S1D and RADARSAT, which has
#         RADARSAT-1 and RADARSAT-2. This field allows users to search for
#         Sentinel-1 data, for example, without needing to specify which specific
#         platform the data came from.
#
#     sar:instrument:
#         required
#         string
#         Name of the sensor used, although for Items which contain data from
#         multiple sensors this could also name multiple sensors.
#
#     sar:instrument_mode:
#         required
#         string
#         The name of the sensor acquisition mode that is commonly used. This
#         should be the short name, if available. For example, WV for "Wave mode"
#         of Sentinel-1 and Envisat ASAR satellites.
#         example: "WV"
#
#     sar:frequency_band:
#         required
#         string
#         The common name for the frequency band to make it easier to search for
#         bands across instruments. See section "Common Frequency Band Names" for
#         a list of accepted names.
#         "P", "L", "S", "C", "X", "Ku", "K", "Ka"
#
#     sar:center_wavelength:
#         number
#         The center wavelength of the instrument, in centimeters (cm).
#
#     sar:center_frequency:
#         number
#         The center frequency of the instrument, in gigahertz (GHz).
#
#     sar:polarization:
#         required
#         array of strings (length of 1 to 4)
#         A single polarization or a polarization combinations specified as array.
#         For single polarized radars one of `HH`, `VV`, `HV` or `VH` must be set.
#         Fully polarimetric radars add all four polarizations to the array. Dual
#         polarized radars and alternating polarization add the corresponding
#         polarizations to the array, for instance for `HH+HV` add both `HH`
#         and `HV`.
#         "HH", "VV", "HV", "VH"
#
#     sar:bands:
#         array of objects
#         This is a list of the available bands where each item is a Band Object.
#
#     sar:type:
#         required
#         string
#         The product type, for example `RAW`, `GRD`, `OCN` or `SLC` for
#         Sentinel-1.
#
#     sar:resolution:
#         array of numbers (minimum = 0, length = 2)
#         The maximum ability to distinguish two adjacent targets, in
#         meters (m). The first element of the array is the range resolution,
#         the second element is the azimuth resolution.
#
#     sar:pixel_spacing:
#         array of numbers (minimum = 0, length = 2)
#         The distance between adjacent pixels, in meters (m). The first
#         element of the array is the range pixel spacing, the second element
#         is the azimuth pixel spacing. Strongly RECOMMENDED to be specified
#         for products of type `GRD`.
#
#     sar:looks:
#         array of numbers (minimum = 0, length = 2 or 3)
#         The number of groups of signal samples (looks). The first element of
#         the array must be the number of range looks, the second element must be
#         the number of azimuth looks, the optional third element is the
#         equivalent number of looks (ENL).
#
#     sar:absolute_orbit:
#         array of numbers and arrays of numbers (with length = 2 of the array in the array and minimum = 0)
#         A list of absolute orbit numbers. Usually corresponds to the orbit
#         count within the orbit cycle (e.g. ALOS, ERS-1/2, JERS-1, and
#         RADARSAT-1, Sentinel-1). For UAVSAR it is the Flight ID. A range can be
#         specified as two element array in the array, e.g. `[25101, [25131, 25140]]`
#         would be 25101 and 25131 to 25140.
#     """
#     # TODO Doppelpunkte!!!
#     def __init__(
#             self, sar_platform: str,  sar_constellation: str = None,
#             sar_instrument: str, sar_instrument_mode: str,
#             sar_frequency_band: str, sar_center_wavelength: float = None,
#             sar_center_frequency: float = None,
#             sar_polarization: Optional[Tuple[str, Optional[str], Optional[str], Optional[str]]] = None,
#             sar_bands: SarBands = SarBands(), sar_type: str,
#             sar_resolution: Optional[Tuple[float, float]] = None,
#             sar_pixel_spacing: Optional[Tuple[float, float]] = None,
#             sar_looks: Optional[Tuple[int, int, Optinal[int]]] = None,
#             sar_absolute_orbit: Optional[List[Union[int, List[int]]]] = None
#             ):
#
#         self.sar:platform = sar_platform
#         self.sar:constellation = sar_constellation
#         self.sar:instrument = sar_instrument
#         self.sar:instrument_mode = sar_instrument_mode
#         self.sar:frequency_band = sar_frequency_band
#         self.sar:center_wavelength = sar_center_wavelength
#         self.sar:center_frequency = sar_center_frequency
#         self.sar:polarization = sar_polarization
#         self.sar:bands = sar_bands
#         self.sar:type = sar_type
#         self.sar:resolution = sar_resolution
#         self.sar:pixel_spacing = sar_pixel_spacing
#         self.sar:looks = sar_looks
#         self.sar:absolute_orbit = sar_absolute_orbit


# class CollectionEO(JsonableObject): TODO Doppelpunkte
#     """
#     eo:gsd:
#         required
#         number
#         The nominal Ground Sample Distance for the data, as measured in meters
#         on the ground. Since GSD can vary across a scene depending on
#         projection, this should be the average or most commonly used GSD in the
#         center of the image. If the data includes multiple bands with different
#         GSD values, this should be the value for the greatest number or most
#         common bands. For instance, Landsat optical and short-wave IR bands are
#         all 30 meters, but the panchromatic band is 15 meters. The eo:gsd
#         should be 30 meters in this case since those are the bands most
#         commonly used.
#
#     eo:platform:
#         required
#         string
#         Unique name of the specific platform the instrument is attached to. For
#         satellites this would be the name of the satellite (e.g., landsat-8,
#         sentinel-2A), whereas for drones this would be a unique name for the
#         drone.
#
#     eo:constellation:
#         string
#         The name of the group of satellites that have similar payloads and have
#         their orbits arranged in a way to increase the temporal resolution of
#         acquisitions of data with similar geometric and radiometric
#         characteristics. Examples are the Sentinel-2 constellation, which has
#         S2A and S2B and RapidEye. This field allows users to search for
#         Sentinel-2 data, for example, without needing to specify which specific
#         platform the data came from.
#
#     eo:instrument:
#         required
#         string
#         The name of the sensor used, although for Items which contain data from
#         multiple sensors this could also name multiple sensors. For example,
#         data from the Landsat-8 platform is collected with the OLI sensor as
#         well as the TIRS sensor, but the data is distributed together and
#         commonly referred to as OLI_TIRS.
#
#     eo:epsg:
#         nullable: true
#         number
#         EPSG code of the datasource, `null` if no EPSG code. A Coordinate
#         Reference System (CRS) is the native reference system (sometimes called
#         a 'projection') used by the data, and can usually be referenced using
#         an EPSG code. If the data does not have a CRS, such as in the case of
#         non-rectified imagery with Ground Control Points, `eo:epsg` should be
#         set to `null`. It should also be set to `null` if a CRS exists, but for
#         which there is no valid EPSG code.
#
#     eo:bands:
#         required
#         list of object
#         This is a list of the available bands where each item is a Band Object.
#     """
#     # TODO Doppelpunkte!!!
#     def __init__(self, eo_gsd: int, eo_platform: str, eo_constellation: str = None,
#                     eo_instrument: str, eo_epsg: int = None, eo_bands: List[EOBands] ):
#         self.eo:gsd = eo_gsd
#         self.eo:platform = eo_platform
#         self.eo:constellation = eo_constellation
#         self.eo:instrument = eo_instrument
#         self.eo:epsg = eo_epsg
#         self.eo:bands = eo_bands


class CollectionProviders(JsonableObject):
    """
    name:
        required
        string
        The name of the organization or the individual.

    description:
        string
        Multi-line description to add further provider information such as
        processing details for processors and producers, hosting details for
        hosts or basic contact information. CommonMark 0.28 syntax MAY be used
        for rich text representation.

    roles:
        array of strings
        Roles of the provider. The provider's role(s) can be one or more of the
        following elements:
        * licensor: The organization that is licensing the dataset under the
          license specified in the collection's license field.
        * producer: The producer of the data is the provider that initially
          captured and processed the source data, e.g. ESA for Sentinel-2 data.
        * processor: A processor is any provider who processed data to a
          derived product.
        * host: The host is the actual provider offering the data on their
          storage. There should be no more than one host, specified as last element of the list.

    url:
        string (url-format)
        Homepage on which the provider describes the dataset and publishes
        contact information.
    """

    def __init__(self, name: str, description: str = None,
            roles: List[str] = None, url: str = None):
        self.name = name
        self.description = description
        #if roles:
        #    for role in roles:
        #        if role not in ["producer", "licensor", "processor", "host"]:
        #            es = ErrorSchema(id=str(datetime.now().isoformat()), code=400,
        #                message="The provider's role(s) can be one or more of the following elements: producer, licensor, processor, host")
        #            return make_response(es.to_json(), 400)
        self.roles = roles
        self.url = url


class CollectionEntry(JsonableObject):
    """
    title:
        string (collection_title)
        A short descriptive one-line title for the collection.

    description:
        required
        string (collection_description)
        Detailed multi-line description to fully explain the collection.
        CommonMark 0.28 syntax MAY be used for rich text representation.

    license:
        required
        string (collection_license)
        Collection's license(s) as a SPDX License identifier, SPDX expression,
        or the string proprietary if the license is not on the SPDX license list.
        Proprietary licensed data SHOULD add a link to the license text with the l
        icense relation in the links section (not as a value of this fields).

    stac_version:
        required
        string (stac_version)
        The STAC version the collection implements.

    id:
        required
        string (collection_id) ^[A-Za-z0-9_\-\.~\/]+$
        Identifier for the collection that is unique across the provider.
        MUST match the specified pattern.

    keywords:
        Array of strings (collection_keywords)
        List of keywords describing the collection.

    version:
        string (collection_version)
        Version of the collection.

    providers:
        Array of object (collection_providers)
        A list of providers, which may include all organizations capturing
        or processing the data or the hosting provider. Providers should
        be listed in chronological order with the most recent provider being
        the last element of the list.

    extent:
        required
        object (STAC Collection Extent)
        The object describes the spatio-temporal extents of the Collection.
        Both spatial and temporal extents are required to be specified.

    links:
        required
        Array of object (collection_links)
        Additional links related to this collection.
        Could reference to other meta data formats with additional
        information or a preview image.

    properties:
        required
        STAC Other Extensions (object) or
        STAC EO (Electro-Optical) (object) or
        STAC SAR (object) or
        STAC Scientific (object) (STAC Collection Properties).
        A list of all metadata properties, which are common across the
        whole collection.

    other_properties:
        required
        object (STAC Varying Collection Properties)
        A list of all metadata properties, which don't have common
        values across the whole collection. Therefore it allows to
        specify a summary of the values as extent or set of values.
    """

    # TODO provider not required
    def __init__(self, providers: Optional[CollectionProviders] = None,
                 links: Optional[List[EoLink]] = [EoLink(href="http://www.mundialis.de", title="mundialis", rel="external"),],
                 extent: Optional[CollectionExtent] = CollectionExtent(),
                 title: str = None, description: str = None, license: str = "proprietary",
                 stac_version: str = "0.6.2", id: str = None, version: str = None,
                 keywords: List[str] = None,
                 properties: Optional[CollectionProperties] = CollectionProperties(),
                 dimensions = None):
        self.title = title
        self.description = description
        self.license = license
        self.extent = extent
        self.links = links
        self.stac_version = stac_version
        #pattern = "^[A-Za-z0-9_\-\.~\/]+$"
        #x = re.search(pattern, id)
        #if not x:
        #    es = ErrorSchema(id=str(datetime.now().isoformat()), code=400,
        #        message="The id MUST match the following pattern: %s" % pattern)
        #    return make_response(es.to_json(), 400)
        self.id = id
        self.keywords = keywords
        self.version = version
        self.providers = providers
        self.properties = properties
        if not dimensions:
            dimensions = {"x": {
            "type": "spatial",
            "axis": "x"
        },
            "y": {
            "type": "spatial",
            "axis": "x"
        },
        }
        self.cube___dimensions = dimensions
        # STAC Common Metadata: A list of commonly used fields throughout all domains
        # https://github.com/radiantearth/stac-spec/tree/v0.9.0/item-spec/common-metadata.md
        # Content Extensions: Domain-specific fields for domains such as EO, SAR and point clouds.
        # https://github.com/radiantearth/stac-spec/tree/v0.9.0/extensions/README.md#list-of-content-extensions
        self.summaries = {}


class Collection(JsonableObject):
    """A collection of data description entries
    """

    def __init__(self, collections: List[CollectionEntry],
                 links: Optional[List[EoLink]] = [EoLink(href="http://www.mundialis.de", title="mundialis", rel="external"),]):
        self.collections = collections
        self.links = links

# TODO !!!
# collection_band_description:
#     string
#     Description to fully explain the band, should include processing information.
#     CommonMark 0.28syntax MAY be used for rich text representation.",
#
#
# collection_dimension_type_spatial:
#     string
#     Type of the dimension, always `spatial`.
#     enum: ["spatial"]
#
# collection_dimension_extent_open:
#     array of numbers (minItems: 2, maxItems: 2)
#     If the dimension consists of ordinal values, the extent
#     (lower and upper bounds) of the values as two-dimensional array.
#     Use `null` for open intervals.
#
# collection_dimension_values:
#     array (number/string) (minItems: 1)
#     A set of all potential values, especially useful for nominal values.
#     Important: The order of the values MUST be exactly how the dimension
#     values are also ordered in the data (cube). If the values specify band
#     names, the values MUST be in the same order as they are in the
#     corresponding band fields (i.e. `eo:bands` or `sar:bands`).
#
# collection_dimension_step:
#     number
#     If the dimension consists of interval values, the space between the values.
#     Use `null` for irregularly spaced steps.
#
# collection_dimension_unit:
#     string
#     The unit of measurement for the data, preferably the symbols from SI
#     or UDUNITS.
#
# collection_dimension_reference_system_spatial:
#     string odr number
#     The spatial reference system for the data, specified as EPSG code.
#     Defaults to EPSG code 4326.


class CollectionInformation(CollectionEntry):

    def __init__(self, keywords: Optional[List[str]] = None, version: str = None, **kwargs):
        super(CollectionInformation, self).__init__(**kwargs)

        self.keywords = keywords
        self.version = version
