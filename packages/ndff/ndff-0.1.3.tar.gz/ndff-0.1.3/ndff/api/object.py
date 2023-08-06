import json
import logging
import re

from urllib.parse import urlparse
import shapely.wkt
from datetime import datetime, timedelta
from ..utils import is_uri

log = logging.getLogger(__name__)


class NdffObservation:

    # all fields that should have an URI as value
    URI_FIELDS = (
        'taxon',
        'abundance_schema',
        'determination_method',
        'dataset',
        'biotope',
        'identity',
        'lifestage',
        'subject_type',
        'survey_method',
        'sex',
        'activity',
    )

    OTHER_FIElDS = (
        'abundance_value',
        'period_start',
        'period_stop',
    )

    def __init__(self):
        self.taxon = None  # URI
        self.abundance_schema = None  # URI
        self.abundance_value = None  # any
        self.activity = None  # URI
        self.determination_method = None  # URI
        self.dataset = None  # URI
        self.biotope = None  # URI
        self.identity = None  # URI
        self.lifestage = None  # URI
        self.period_start = None  # ISO datetime str
        self.period_stop = None  # ISO datetime str
        self.sex = None  # URI
        self.subject_type = None  # URI
        self.survey_method = None  # URI

        self.extra_info = []
        self.involved = []

        self.location: dict = None  # a location should always be a valid location dict, never something else!

    def fields(self):
        return self.__dict__

    def get(self, field_name):
        if field_name in self.__dict__:
            if field_name == 'location':
                if self.location:
                    # TODO: create better string representation (eg for Polygon)
                    return str(self.location)
                else:
                    return 'Location ??'
            else:
                return self.__dict__[field_name]
        else:
            return None

    def set(self, field_name: str, field_value):
        # TODO more checks ?
        # ONLY set available properties (NOT adding new ones)
        if field_name in self.__dict__:
            if field_name == 'location' and not isinstance(field_value, dict):
                raise ValueError(f'Not possible to set location for an NdffObservation: value is NOT a (location) dict!')
            self.__dict__[field_name] = field_value
        else:
            raise ValueError(f'Not possible to set "{field_name}" for an NdffObservation: NOT an available property!')

    def set_extra_info(self, key_uri: str, value: str):
        # the key of an extra info field should ALWAYS be an uri! SHOULD BE CHECKED BEFORE SETTING !!!
        # the value can be both a data value or a value mapped to a NDFF uri
        # BOTH should be valid strings, NOT none
        if key_uri and value:
            self.extra_info.append({'key': key_uri, 'value': value})
        else:
            raise ValueError(f'Setting an Extra Info Key/Value, one of them is None: "{key_uri}" - "{value}"')

    def is_valid(self) -> (bool, list):
        errors = []
        none_message = 'Veld "{}" is nog leeg of onbekend'
        not_uri_message = 'Veld "{}" zou een URI moeten zijn: "{}"'
        not_dict_message = 'Veld "{}" zou een "dict" moeten zijn, maar is "{}"'
        missing_location_field = '"Lokatie" zou een veld "{}" moeten hebben'
        wrong_datetime_format = 'Veld "{}": {} zou een isoformaat moeten hebben zoals 2022-01-01T12:12:00'
        periode_wrong_order = 'De start van periode "{}" - "{}" ligt VOOR of OP het eind'
        period_in_future = 'De periode "{}" - "{}" ligt in de toekomst'
        json_error = 'Er is een fout bij het maken van de json van deze waarneming'

        # URI fields:
        for name in self.URI_FIELDS:
            if self.__dict__[name] in (None, '', ' ', '-', '?'):
                errors.append(none_message.format(name))
            elif not is_uri(self.__dict__[name]):
                errors.append(not_uri_message.format(name, self.__dict__[name]))

        # NON uri fields, we can only check for None/Null
        for name in self.OTHER_FIElDS:
            if self.__dict__[name] in (None, '', ' ', '-', '?'):
                errors.append(none_message.format(name))

        # Location related fields:
        # "location": {
        #     "buffer": 5,
        #     "geometry": {
        #         "type": "Point",
        #         "coordinates": [
        #             408241,
        #             78648
        #             ]
        #         }
        #     },
        if self.location in (None, '', ' ', '-', '?'):
            errors.append(none_message.format('location'))
        if not isinstance(self.location, dict):
            errors.append(not_dict_message.format('location', type(self.location)))
        else:
            # ok, we have a dict, check keys
            for field in ['buffer', 'geometry']:
                # check for field key
                if field not in self.location:
                    errors.append(missing_location_field.format(field))
                # check for field value
                else:
                    # TODO better test? Also test if value is number?
                    if 'buffer' in self.location and self.location['buffer'] in ('', None, '-', '?'):
                        if not none_message.format('location_buffer') in errors:
                            errors.append(none_message.format('location_buffer'))

        # TODO further geometry checking...

        # period (period_start and period_stop)
        start = None
        stop = None
        try:
            start = datetime.fromisoformat(self.period_start)
        except Exception as e:
            errors.append(wrong_datetime_format.format('period_start', self.period_start))
        try:
            stop = datetime.fromisoformat(self.period_stop)
        except Exception as e:
            errors.append(wrong_datetime_format.format('period_stop', self.period_stop))
        if self.period_start is None:
            errors.append(none_message.format('period_start'))
        if self.period_stop is None:
            errors.append(none_message.format('period_stop'))
        if start and stop:
            if stop >= datetime.now():
                errors.append(period_in_future.format(self.period_start, self.period_stop))
            if start >= stop:
                errors.append(periode_wrong_order.format(self.period_start, self.period_stop))

        # other fields

        if len(errors) == 0:
            return True, []
        else:
            # trying to insert the 'identity' of this observation
            errors.insert(0, f'Identity: {self.identity}')
            return False, errors

    def to_ndff_observation_json(self, observation_identity=None, observation_dataset=None) -> str:
        """
        The observation_identity and observation_dataset params make it possible
        to override the real identity/dataset content of the observation, thereby
        makeing it easier to create unique observation json for testing...

        Create valid JSON for NDFF based on current values of all fields.
        If the param 'observation_identity' is None, the field 'identity'
        should be a valid identity(-uri).
        If the param 'observation_dataset' is None, the field 'dataset' should
        be a valid dataset(-uri). AND should be available/defined at NDFF

        :param observation_identity (optional):
        :param observation_dataset (optional):
        :return: NDFF json as string
        """
        # json = '''{"abundanceSchema": "http://ndff-ecogrid.nl/codes/scales/exact_count",
        #     "abundanceValue": 1,
        #     "activity": "http://ndff-ecogrid.nl/codes/domainvalues/observation/activities/calling",
        #     "determinationMethod": "http://ndff-ecogrid.nl/codes/domainvalues/observation/determinationmethods/550",
        #     "extrainfo": [],
        #     "dataset": "http://notatio.nl/dataset/2",
        #     "biotope": "http://ndff-ecogrid.nl/codes/domainvalues/location/biotopes/unknown",
        #     "identity": "http://notatio.nl/waarneming/7500",
        #     "involved": [
        #         {
        #         "involvementType": "http://ndff-ecogrid.nl/codes/involvementtypes/data_owner",
        #         "person": "http://telmee.nl/contacts/persons/1261085"
        #         }
        #     ],
        #     "lifestage": "http://ndff-ecogrid.nl/codes/domainvalues/observation/lifestages/509",
        #     "location": {
        #         "buffer": 5,
        #         "geometry": {
        #             "type": "Point",
        #             "coordinates": [
        #                 408241,
        #                 78648
        #                 ]
        #             }
        #         },
        #     "periodStart": "2014-08-29 01:22:00",
        #     "periodStop": "2014-08-29 01:22:00",
        #     "sex": "http://ndff-ecogrid.nl/codes/domainvalues/observation/sexes/undefined",
        #     "subjectType": "http://ndff-ecogrid.nl/codes/subjecttypes/live/individual",
        #     "surveyMethod": "http://ndff-ecogrid.nl/codes/domainvalues/survey/surveymethods/na",
        #     "taxon": "http://ndff-ecogrid.nl/taxonomy/taxa/pipistrellusnathusii",
        #     "extrainfo": [
        #         {
        #           "key": "http://ndff-ecogrid.nl/codes/keys/external/location_id",
        #           "value": "NL09_GROO6140002"
        #         },
        #         {
        #           "key": "http://ndff-ecogrid.nl/codes/keys/external/original_visit_id",
        #           "value": "NL09_GROO6140002_2014_7_21_VISB1_1"
        #         }
        #     ]
        #
        # }

        if not self.is_valid()[0]:
            raise ValueError(self.is_valid()[1])

        data = {}

        if observation_identity:
            data['identity'] = observation_identity
        else:
            data['identity'] = self.identity
        if observation_dataset:
            data['dataset'] = observation_dataset
        else:
            data['dataset'] = self.dataset
        data['abundanceSchema']         = self.abundance_schema
        data['abundanceValue']          = self.abundance_value
        data['activity']                = self.activity
        data['determinationMethod']     = self.determination_method
        # dataset ^
        data['biotope']                 = self.biotope
        # identity ^
        data['lifestage']               = self.lifestage
        data['sex']                     = self.sex
        data['subjectType']             = self.subject_type
        data['surveyMethod']            = self.survey_method
        data['taxon']                   = self.taxon
        # periods should be datetime objects in self.period - tuple
        data['periodStart']             = self.period_start
        data['periodStop']              = self.period_stop
        data['location']                = self.location

        # note: this is the data holder for the lists in the json (NOT fields from record or observation)
        data['extrainfo']               = self.extra_info
        data['involved']                = self.involved
        # for key in self.data.keys():
        #     list_field = None
        #     kv1 = None
        #     kv2 = None
        #     if 'extra_info_identity_' in key:
        #         list_field = 'extrainfo'
        #         if self.data[key] is not None:
        #             kv1 = ('identity', self.data[key])
        #             kv2 = ('value', self.data['extra_info_value_'+key.replace('extra_info_identity_', '')])
        #     elif 'involved_type_' in key:
        #         list_field = 'involved'
        #         if self.data[key] is not None:
        #             kv1 = ('involvementType', self.data[key])
        #             kv2 = ('person', self.data['involved_person_'+key.replace('involved_type_', '')])
        #     if list_field and kv1 and kv2:
        #         data[list_field].append({kv1[0]: kv1[1], kv2[0]: kv2[1]})

        return json.dumps(data, indent=2)


class NdffObservation1:

    EPSG_4326 = 'EPSG:4326'
    EPSG_28992 = 'EPSG:28992'

    @staticmethod
    def from_dict(valid_ndff_dict):
        o = NdffObservation1()
        o.taxon = valid_ndff_dict['taxon']
        o.abundance_schema = valid_ndff_dict['abundance_schema']
        o.location = valid_ndff_dict['location']
        return o

    def __init__(self):
        self._taxon = None
        self._abundance_schema = None
        # self._abundance_value = None
        # self._fields['activity'] = 'activity'
        # self._fields['determination_method'] = 'determination_method'
        # self._fields['dataset'] = 'dataset'
        # self._fields['biotope'] = 'biotope'
        # self._fields['identity'] = 'identity'
        # self._fields['lifestage'] = 'lifestage'
        # self._fields['period_start'] = 'period_start'
        # self._fields['period_stop'] = 'period_stop'
        # self._fields['sex'] = 'sex'
        # self._fields['subject_type'] = 'subject_type'
        # self._fields['survey_method'] = 'survey_method'
        #
        # self._fields['extra_info_identity_1'] = 'extra_info_identity_1'
        # self._fields['extra_info_value_1'] = 'extra_info_value_1'
        # self._fields['extra_info_identity_2'] = 'extra_info_identity_2'
        # self._fields['extra_info_value_2'] = 'extra_info_value_2'
        # # Note: can be more (via use of 'master', but should ALWAYS start with 'extra_info_identity_' and 'extra_info_value_')
        #
        # self._fields['involved_person_1'] = 'involved_person_1'
        # self._fields['involved_type_1'] = 'involved_type_1'
        # self._fields['involved_person_2'] = 'involved_person_2'
        # self._fields['involved_type_2'] = 'involved_type_2'
        # # Note: can be more (via use of 'master', but should ALWAYS start with 'involved_person_' and 'involved_type_')

        self._location: dict = {}
        # buffer is more or less a separate thing?
        self._location_buffer: float = 0

    def is_valid(self) -> (bool, list):
        errors = []
        none_message = 'Veld "{}" is nog leeg of onbekend: "{}"'
        not_uri_message = 'Veld "{}" zou een URI moeten zijn: "{}"'
        not_dict_message = 'Veld "{}" zou een "dict" moeten zijn, maar is "{}"'
        missing_location_field = 'Locatie zou een veld "{}" moeten hebben'


        # URI fields:
        for field, name in [
            (self._taxon, 'taxon'),
            (self._abundance_schema, 'abundance_schema')
        ]:
            if field is None:
                errors.append([none_message.format(name, field)])
            elif not is_uri(field):
                errors.append([not_uri_message.format(name, field)])

        # "location": {
        #     "buffer": 5,
        #     "geometry": {
        #         "type": "Point",
        #         "coordinates": [
        #             408241,
        #             78648
        #             ]
        #         }
        #     },
        if self.location is None:
            errors.append([none_message.format('location', self.location)])
        if not isinstance(self.location, dict):
            errors.append([not_dict_message.format('location', type(self.location))])
        else:
            # ok, we have a dict, check keys
            for field in ['buffer', 'geometry']:
                if field not in self.location:
                    errors.append(missing_location_field.format(field))
        # TODO further geometry checking...

        # period (period_start and period_stop)

        # other fields

        if len(errors) == 0:
            return True, []
        else:
            return False, errors

    @property
    def taxon(self) -> str:
        return self._taxon

    @taxon.setter
    def taxon(self, taxon: str):
        self._taxon = taxon

    @property
    def abundance_schema(self) -> str:
        return self._abundance_schema

    @abundance_schema.setter
    def abundance_schema(self, abundance_schema: str):
        self._abundance_schema = abundance_schema

    @property
    def location(self) -> dict:
        return self._location

    @location.setter
    def location(self, location: dict):
        self._location = location



class NdffObservation0:
    """
    An NdffObservation is a class which can hold one Waarneming
    So it is valid if it can serialize itself to json and be accepted by ndff as valid
    It should also be possible to create an instance based on a valid Waarneming.json
    Constructors could be:
    - creation from a dictionary with strict defined keys
    - creation from a Waarneming json

    Still considering if NdffObservation should be a DataClass (so as flat as possible)
    OR a normal class
    Argument against DataClass is: the json export is nested, we we should create a mapping

    All attribute values should be valid uri's

    json = '{"abundanceSchema": "http://ndff-ecogrid.nl/codes/scales/exact_count",
        "abundanceValue": 1,
        "activity": "http://ndff-ecogrid.nl/codes/domainvalues/observation/activities/calling",
        "determinationMethod": "http://ndff-ecogrid.nl/codes/domainvalues/observation/determinationmethods/550",
        "extrainfo": [
            {
            "key": "http://ndff-ecogrid.nl/codes/keys/observation/collectionnr",
            "value": 1
            }
        ],
        "dataset": "http://notatio.nl/dataset/2",
        "biotope": "http://ndff-ecogrid.nl/codes/domainvalues/location/biotopes/unknown",
        "identity": "http://notatio.nl/waarneming/7500",
        "involved": [
            {
            "involvementType": "http://ndff-ecogrid.nl/codes/involvementtypes/data_owner",
            "person": "http://telmee.nl/contacts/persons/1261085"
            }
        ],
        "lifestage": "http://ndff-ecogrid.nl/codes/domainvalues/observation/lifestages/509",
        "location": {
            "buffer": 5,
            "geometry": {
                "type": "Point",
                "coordinates": [
                    408241,
                    78648
                    ]
                }
            },
        "periodStart": "2014-08-29 01:22:00",
        "periodStop": "2014-08-29 01:22:00",
        "sex": "http://ndff-ecogrid.nl/codes/domainvalues/observation/sexes/undefined",
        "subjectType": "http://ndff-ecogrid.nl/codes/subjecttypes/live/individual",
        "surveyMethod": "http://ndff-ecogrid.nl/codes/domainvalues/survey/surveymethods/na",
        "taxon": "http://ndff-ecogrid.nl/taxonomy/taxa/pipistrellusnathusii"
        "dwelling": "http://ndff-ecogrid.nl/codes/domainvalues/observation/dwellings/unknown"
    }

    """
    # good enough test for wkt
    # https://regex101.com/
    # currently only "POINT (145918.0769337003 389302.11025674635)" like strings are valid (so UPPERCASE POINT only)
    # OR optional a SRID=4326; in front (EWKT): SRID=4326;POINT (4.67979621887207 51.67397308349609)
    # TODO: QGIS expressions does NOT create POINT but Point (note caps): better to have a more forgiven regexp?
    valid_wkt_point_regex = re.compile(r"(SRID=\d+;)?POINT\s*\(.+\s.+\)", re.MULTILINE | re.UNICODE)
    valid_wkt_multipoint_regex = re.compile(r"(SRID=\d+;)?MULTIPOINT\s*\(.+\s.+\)", re.MULTILINE | re.UNICODE)
    valid_wkt_polygon_regex = re.compile(r"(SRID=\d+;)?POLYGON\s*\(.+\s.+\)", re.MULTILINE | re.UNICODE)

    EPSG_4326 = 'EPSG:4326'
    EPSG_28992 = 'EPSG:28992'

    # fields in ndff_observation hold a list with:
    # field: text,url1,url2,description,ndff_fieldname
    #FIELD_COL_NAME
    FIELD_COL_TEXT = 0
    FIELD_COL_URL1 = 1
    FIELD_COL_URL2 = 2
    FIELD_COL_DESCRIPTION = 3
    FIELD_COL_NDFF_NAME = 4
    FIELD_COL_CHANGE_DATA = 5

    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

    non_uri_values = ['abundance_value', 'period_start', 'period_stop',
     'location', 'location_buffer', 'location_x', 'location_y']

    def __init__(self, record={}, mappings={}, defaults={}, master={}, data_mappings={}):
        """
        Create an observation from a dictionary of exact(!) fitting key values

        :param master:
        :param record: a flat dict data record (column/field name -> column/field value)
        :param mappings: a dict of field -> NDFFObservation field
        :param defaults: a dict of NDFFObservation field -> default value
        :param master: a dict of NDFFObservation fields -> a list/dict(?) of
                        - fieldname, text to use in gui, url1, url 2 to search for, description
                        when actually used will replace self.data
        """

        self.data_mappings = data_mappings

        if len(master.keys()) > 0:
            self._fields = master
        else:
            self._fields = {}
            self._fields['taxon'] = 'taxon'
            self._fields['abundance_schema'] = 'abundance_schema'
            self._fields['abundance_value'] = 'abundance_value'
            self._fields['activity'] = 'activity'
            self._fields['determination_method'] = 'determination_method'
            self._fields['dataset'] = 'dataset'
            self._fields['biotope'] = 'biotope'
            self._fields['identity'] = 'identity'
            self._fields['lifestage'] = 'lifestage'
            self._fields['period_start'] = 'period_start'
            self._fields['period_stop'] = 'period_stop'
            self._fields['sex'] = 'sex'
            self._fields['subject_type'] = 'subject_type'
            self._fields['survey_method'] = 'survey_method'
    
            self._fields['extra_info_identity_1'] = 'extra_info_identity_1'
            self._fields['extra_info_value_1'] = 'extra_info_value_1'
            self._fields['extra_info_identity_2'] = 'extra_info_identity_2'
            self._fields['extra_info_value_2'] = 'extra_info_value_2'
            # Note: can be more (via use of 'master', but should ALWAYS start with 'extra_info_identity_' and 'extra_info_value_')
    
            self._fields['involved_person_1'] = 'involved_person_1'
            self._fields['involved_type_1'] = 'involved_type_1'
            self._fields['involved_person_2'] = 'involved_person_2'
            self._fields['involved_type_2'] = 'involved_type_2'
            # Note: can be more (via use of 'master', but should ALWAYS start with 'involved_person_' and 'involved_type_')

            # Note: data can be a list of (x,y), a (E)WKT string (or a QGIS geometry?
            self._fields['location'] = 'location'
            self._fields['location_x'] = 'location_x'
            self._fields['location_y'] = 'location_y'
            # buffer is more or less a separate thing?
            self._fields['location_buffer'] = 'location_buffer'

        # fill data with fields (not data-values yet) defined above, AND in the (optional) master object build via the ndff_observation.csv
        self.data = {}
        for field in self._fields.keys():
            self.data[field] = None

        # copy the values from the record dict using the exact right keys and values
        for key in record:
            if key in self.data.keys():
                self.data[key] = record[key]
            # ONLY if a a field misses, try to see if it is in mappings:
            elif key in mappings:
                # ok, we have a mapping here,say:
                # subject_type is named subject in the records:  { subject: subject_type }
                self.data[mappings[key]] = record[key]

        # check for defaults and set as default IF available
        for key in defaults:
            self.data[key] = defaults[key]

        # handle data mappings: go over all fields, and if NOT an uri, check if
        # there is a mapped value for that field
        for field, value in self.data.items():
            log.debug(f'Data mapping: "{field}" "{value}')
            if value and field not in self.non_uri_values and not is_uri(value):
                if field in self.data_mappings and value in self.data_mappings[field]:
                    # YES, hopefully an uri in the mappings:
                    self.data[field] = self.data_mappings[field][value]

        self.geom = None
        self.crs = self.EPSG_4326  # defaulting to EPSG:4326 == Lat Lon coordinates
        # naive creation of geom (and setting of crs), no further checking
        self._create_geom()

        self.period = None
        # naive try to create a period here
        self._create_period()

    def __repr__(self):
        return f"""NdffObservation: {self.geom}
        {self.data}"""

    def _set_crs(self, coordinates):
        if float(max(coordinates)) < 200:
            self.crs = self.EPSG_4326
        elif float(max(coordinates)) < 620000:
            self.crs = self.EPSG_28992
        else:
            raise Exception("Coordinates outside of EPSG:4326 or EPSG:28992 range")

    def get_crs(self) -> str:
        return self.crs

    def _create_geom(self):
        """
        Create self.geom: a location dict from location_buffer
            - either the location
            - or the location_x AND location_y fields
            - ore set via 'set(location, wkt)'

        "location": {
            "buffer": 5,
            "geometry": {
                "type": "Point",
                "coordinates": [
                    408241,
                    78648
                    ]
                }
            }

        :returns: True in case the creation succeeded, False in case of a failure
        """
        # TODO further location creation
        # TODO handle other geometries: POLYGON and POINT
        # TODO fix tests, as they succeed while not yet implemented other types..
        # TODO fix the use of shapely, we do NOT want the need of shapely (in the plugin)
        if isinstance(self.data['location'], dict):
            # ok apparently the data is already a dict...
            # this dict should have a buffer already:
            if self.data['location']['buffer']:
                self.data['location_buffer'] = self.data['location']['buffer']
            else:
                return False
            self.geom = self.data['location']
        else:
            # going to create the geometry dict/json here ourselves
            # check if we have a x/y or a wkt geom
            if self.data['location_x'] is not None and self.data['location_y'] is not None:
                # ok we have an x and y column here...
                self.geom = {'geometry': {}}
                self.geom['geometry']['type'] = 'Point'
                try:
                    self.geom['geometry']['coordinates'] = [float(self.data['location_x']), float(self.data['location_y'])]
                except Exception as e:
                    log.debug(f'Error creating a geometry from "{self.data["location_x"]}" and "{self.data["location_y"]}": {e}')
                    return False
            elif isinstance(self.data['location'], str):
                # can be WKT or EWKT
                # BUT Shapely can ONLY load a WKT string
                # so remove the SRID=28992; part from it in case of EWKT
                if 'SRID' in self.data['location']:
                    self.data['location'] = self.data['location'].split(';')[1]
                if self.is_valid_wkt_point(self.data['location']):
                    try:
                        shapely_point = shapely.wkt.loads(self.data['location'])
                        self.geom = {}
                        self.geom['geometry'] = {}
                        self.geom['geometry']['type'] = 'Point'
                        self.geom['geometry']['coordinates'] = [float(shapely_point.x), float(shapely_point.y)]
                    except Exception as e:
                        log.debug(f'Error creating a geometry from {self.data["location"]}: {e}')
                        return False
                else:
                    # TODO
                    log.debug(f'Error creating a geometry from {self.data["location"]}')
                    return False

                # elif self.is_valid_wkt_multipoint(self.data['location']):
                #     self.geom['geometry']['type'] = 'MultiPoint'
                #     try:
                #         shapely_multipoint = shapely.wkt.loads(self.data['location'])
                #         self.geom['geometry']['coordinates'] = shapely_multipoint.coords  # will not work because multi does not create
                #         log.debug(self.geom['geometry']['coordinates'])
                #     except Exception as e:
                #         log.debug(f'Error creating a geometry from {self.data["location"]}: {e}')
                #         return False

            else:
                log.debug('(Yet) unknown geometry type in your wkt...')
                return False

            # check if user has set a default buffer or a field to use as buffer:
            if self.data['location_buffer']:
                try:
                    self.geom['buffer'] = int(self.data['location_buffer'])
                except Exception as e:
                    log.debug(f'Error creating a buffer value from "{self.data["location_buffer"]}": {e}')
                    return False
            else:
                return False
            # else:
            #     # TODO what is a good default buffer here???
            #     self.geom['buffer'] = 10

        if self.geom and 'geometry' in self.geom and 'coordinates' in self.geom['geometry']:
            # ok we have a geometry with coordinates....
            self._set_crs(self.geom['geometry']['coordinates'])
            # all well, return True
            return True

        return False

    def get(self, field_name) -> str:
        return self.data[field_name]

    def set(self, field_name: str, field_value: str):
        # TODO checks
        self.data[field_name] = field_value

        # Special case: geometry: try to create a geom...
        if 'location' in field_name:
            self.geom = None
            if field_name == 'location':
                # clean up location_x and location_y
                self.data['location_x'] = None
                self.data['location_y'] = None
            elif field_name == 'location_x' or field_name == 'location_y':
                # clean up location
                self.data['location'] = None
            return self._create_geom()
        # Special case: period: fix period(s)
        if 'period' in field_name:
            return self._create_period()

        return field_value  # or False if failing ? or Exception?

    def _create_period(self):
        """
        Try to create a valid period from either:
        - only a start DATE(Time): (add Time if needed) add a stop datetime+1min)
        - only an end DATE(Time): (add Time if needed) and a start datetime-1min)

        :returns: True in case the creation succeeded, False in case of a failure
        """

        # period_start and period_stop
        if self.data['period_start'] is None and self.data['period_stop'] is None:
            # mmm, apparently nothing is set... non valid record ?
            return False
        try:
            # only a period_start is set: add one minute to it and make that period_stop
            if self.data['period_start'] and self.data['period_stop'] is None:
                start = self.datetimestring_to_datetime(self.data['period_start'])
                end = start + timedelta(minutes=1)
            # only a period_end is set: substract one minute to it and make that period_start
            elif self.data['period_stop'] and self.data['period_start'] is None:
                end = self.datetimestring_to_datetime(self.data['period_stop'])
                # substract one minute
                start = end - timedelta(minutes=1)
            else:
                start = self.datetimestring_to_datetime(self.data['period_start'])
                end = self.datetimestring_to_datetime(self.data['period_stop'])
            # Ok, we should have a valid start AND end now...:
            self.period = (start, end)
        except ValueError as v:
            return False
        return self.period

    @staticmethod
    def datetimestring_to_datetime(date_only_or_datetime_string):
        if len(date_only_or_datetime_string.strip()) < 11:
            dt = datetime.strptime(date_only_or_datetime_string, '%Y-%m-%d')
            dt = dt.replace(hour=12, minute=00, second=00)
        elif len(date_only_or_datetime_string.strip()) < 20:
            #dt = datetime.strptime(date_only_or_datetime_string, NdffObservation.DATETIME_FORMAT)
            # 2022-01-01T12:12:00 OR 2022-01-01T12:12:00 both are 'ISO-format' :-(
            dt = datetime.fromisoformat(date_only_or_datetime_string)
        else:
            raise ValueError(f'Trying to create a datetime from a date(time)string which does not to be OK: {date_only_or_datetime_string}')
        return dt

    def is_valid_wkt_point(self, location_string: str) -> bool:
        # 'POINT (145918.0769337003 389302.11025674635)'
        if self.valid_wkt_point_regex.match(location_string.upper()):
            return True
        return False

    def is_valid_wkt_multipoint(self, location_string: str) -> bool:
        #
        if self.valid_wkt_multipoint_regex.match(location_string.upper()):
            return True
        return False

    def is_valid_wkt_polygon(self, location_string: str) -> bool:
        # POLYGON ((4.41042 51.86444, 4.41042 51.86444, 4.410441 51.86443, 4.41044 51.86444, 4.41042 51.86444))
        if self.valid_wkt_polygon_regex.match(location_string.upper()):
            return True
        return False

    # TODO We want to return BOTH the validity as a bool, BUT also the reason
    # BUT returning a tuple, means we have to do: "o.is_valid()[0]"
    # which is ugly, we just want: "o.is_valid()"
    # Idea's ??
    def is_valid(self, full_check=False) -> tuple:
        """
        :return: A tuple with (True) return True, and (False, reason) if False
        """
        # some easy check for:
        #  - number of fields,
        #  - and none of these are None
        #  - there is at least one 'involved' item (which should be a dict too)
        #  - there is a WKT Point in it

        # TODO period_start and period_stop format testing

        # geometry check
        location_ok = self.is_valid_location()
        log.warning(f'Location check: {location_ok} {self.get("location")} {self.get("location_x")} {self.get("location_y")}')
        if not location_ok[0]:
            return location_ok

        # time check
        times_ok = self.is_valid_time_interval(self.get('period_start'), self.get('period_stop'))
        if not times_ok[0]:
            return times_ok

        for key, val in self.data.items():
            if 'involved_' in key or 'extra_info_' in key:
                # all optional: CAN be None ...
                pass
            elif key in ('location', 'location_x', 'location_y'):
                # either location is not None
                # OR location_x AND location_y are both not None
                # will be checked later
                pass
            elif val is None:
                reason = f'Field {key} is still None: Observation not inited ok.'
                log.warning(reason)
                return False, reason

        # Check if value is an uri..
        if full_check:
            # go over all uri-values and check if these are valid uri's
            for key in self.data.keys():
                if key in self.non_uri_values:
                    pass
                elif 'extra_info_' in key or 'involved_' in key:
                    # either None OR an uri
                    if self.data[key] is not None and not is_uri(f'{self.data[key]}'):
                        reason = f'{key} is NOT an uri: {self.data[key]}'
                        log.warning(reason)
                        return False, reason
                elif not is_uri(f'{self.data[key]}'):
                    reason = f'{key} is NOT an uri: {self.data[key]}'
                    log.warning(reason)
                    return False, reason

        return True, True

    def is_valid_time_interval(self, period_start, period_stop) -> tuple:
        """
        Function to do some checking on the time interval (period_start and period_stop)

        These should be a iso-datetime STRING like  YYYY-MM-DDTHH:mm:ss.sssZ
        ?? OR only DATE (iso-date) ??


        :param time:
        :return: A tuple with (True) return True, and (False, reason) if False
        """

        # check if both arguments are type string
        if not isinstance(period_start, str):
            return False, 'The period_start does not seem to be an iso string'
        if not isinstance(period_stop, str):
            return False, 'The period_stop does not seem to be an iso string'

        # check if it is either an iso-datetime or a iso-date

        # if only iso-date it should be "fixed"...? to 12:00 ???

        # if both iso_datetime: there should be an interval of 1 minute or 1 hour

        # all OK:
        return True, True


    def is_valid_location(self) -> tuple:
        """
        Function to do some checking on the location (geometry) field

        Note: this is a string or a dict, NOT a QgsGeometry!!

        :return: A tuple with (True) return True, and (False, reason) if False
        """
        # valid locations:
        # - a location_x and a location_y in the same crs(!)
        # - a location as wkt or ewkt string

        # TODO?
        # - ?? a location dict ready to be used in json ??  <= don't think so
        if self.get('location_x') and self.get('location_y'):
            pass
        elif self.get('location'):
            pass
        else:
            return False, 'No valid location for this record yet...'

        # try to reset self.geom:
        if not self._create_geom():
            return False, "Location fields seem to be OK, but errors creating a geom from it..."
        # all OK:
        return True, True

    def fields(self):
        return self._fields

    def to_dict(self):
        return self.data

    def to_ndff_observation_json(self, observation_identity=None, observation_dataset=None) -> str:
        """
        Create valid JSON for NDFF based on current values of all fields.
        If the param 'observation_identity' is None, the field 'identity'
        should be a valid identity(-uri).
        If the param 'observation_dataset' is None, the field 'dataset' should
        be a valid dataset(-uri). AND should be available/defined at NDFF

        :param observation_identity (optional): 
        :param observation_dataset (optional):
        :return: NDFF json as string
        """
        # json = '''{"abundanceSchema": "http://ndff-ecogrid.nl/codes/scales/exact_count",
        #     "abundanceValue": 1,
        #     "activity": "http://ndff-ecogrid.nl/codes/domainvalues/observation/activities/calling",
        #     "determinationMethod": "http://ndff-ecogrid.nl/codes/domainvalues/observation/determinationmethods/550",
        #     "extrainfo": [],
        #     "dataset": "http://notatio.nl/dataset/2",
        #     "biotope": "http://ndff-ecogrid.nl/codes/domainvalues/location/biotopes/unknown",
        #     "identity": "http://notatio.nl/waarneming/7500",
        #     "involved": [
        #         {
        #         "involvementType": "http://ndff-ecogrid.nl/codes/involvementtypes/data_owner",
        #         "person": "http://telmee.nl/contacts/persons/1261085"
        #         }
        #     ],
        #     "lifestage": "http://ndff-ecogrid.nl/codes/domainvalues/observation/lifestages/509",
        #     "location": {
        #         "buffer": 5,
        #         "geometry": {
        #             "type": "Point",
        #             "coordinates": [
        #                 408241,
        #                 78648
        #                 ]
        #             }
        #         },
        #     "periodStart": "2014-08-29 01:22:00",
        #     "periodStop": "2014-08-29 01:22:00",
        #     "sex": "http://ndff-ecogrid.nl/codes/domainvalues/observation/sexes/undefined",
        #     "subjectType": "http://ndff-ecogrid.nl/codes/subjecttypes/live/individual",
        #     "surveyMethod": "http://ndff-ecogrid.nl/codes/domainvalues/survey/surveymethods/na",
        #     "taxon": "http://ndff-ecogrid.nl/taxonomy/taxa/pipistrellusnathusii"
        #     "dwelling": "http://ndff-ecogrid.nl/codes/domainvalues/observation/dwellings/unknown"
        # }
        if observation_identity:
            self.data['identity'] = observation_identity
        if observation_dataset:
            self.data['dataset'] = observation_dataset
        if not self.is_valid():
            raise ValueError
        data = {}
        data['abundanceSchema']         = self.data['abundance_schema']
        data['abundanceValue']          = self.data['abundance_value']
        data['activity']                = self.data['activity']
        data['determinationMethod']     = self.data['determination_method']
        data['dataset']                 = self.data['dataset']
        data['biotope']                 = self.data['biotope']
        data['identity']                = self.data['identity']
        data['lifestage']               = self.data['lifestage']
        data['sex']                     = self.data['sex']
        data['subjectType']             = self.data['subject_type']
        data['surveyMethod']            = self.data['survey_method']
        data['taxon']                   = self.data['taxon']
        # periods should be datetime objects in self.period - tuple
        data['periodStart']             = self.period[0].strftime(NdffObservation.DATETIME_FORMAT)
        data['periodStop']              = self.period[1].strftime(NdffObservation.DATETIME_FORMAT)

        data['location']                = self.geom

        # note: this is the data holder for the lists in the json (NOT fields from record or observation)
        data['extrainfo']               = []
        data['involved']                = []
        for key in self.data.keys():
            list_field = None
            kv1 = None
            kv2 = None
            if 'extra_info_identity_' in key:
                list_field = 'extrainfo'
                if self.data[key] is not None:
                    kv1 = ('identity', self.data[key])
                    kv2 = ('value', self.data['extra_info_value_'+key.replace('extra_info_identity_', '')])
            elif 'involved_type_' in key:
                list_field = 'involved'
                if self.data[key] is not None:
                    kv1 = ('involvementType', self.data[key])
                    kv2 = ('person', self.data['involved_person_'+key.replace('involved_type_', '')])
            if list_field and kv1 and kv2:
                data[list_field].append({kv1[0]: kv1[1], kv2[0]: kv2[1]})

        return json.dumps(data, indent=2)


class NdffResult(dict):

    # CREATE TABLE public.ndff_log
    # (
    #   id serial,
    #   object_type character varying,
    #   object_id integer,  -- identiy uri
    #   ndff_uri character varying,
    #   http_method character varying,
    #   http_status character varying,
    #   http_response character varying,
    #   tstamp timestamp with time zone
    # )

    def __init__(self,
                 waarneming_id,
                 object_type,
                 object_id,
                 ndff_uri,
                 http_method,
                 http_status,
                 http_response,
                 id=None,
                 tstamp=None):
        super().__init__()
        logging.debug('Initting NdffResult')

        # temporary?
        # remove query part from nddf_uri
        # after searching the uri's contained ?format=javascript
        o = urlparse(ndff_uri)
        ndff_uri = o.scheme + "://" + o.netloc + o.path
        self['waarneming_id'] = waarneming_id
        self['id'] = id
        self['object_type'] = object_type
        self['object_id'] = object_id
        self['ndff_uri'] = ndff_uri
        self['http_method'] = http_method
        self['http_status'] = http_status
        self['http_response'] = json.dumps(http_response)
        self['tstamp'] = tstamp

    # def print(self):
    #     print('\n** NDFFresult ID: {} **'.format(self['id']))
    #     super().print()
