from ..api import (
    Api,
    NdffObservation,
)
from ..datasource.base import DataSource
from ..utils import is_uri
from pathlib import Path
import shapely.wkt
from datetime import datetime, timedelta
import csv
import re
import logging
log = logging.getLogger(__name__)


class NdffConnector:
    """
    A NdffConnector is the bridge between the NdffApi and Datasource
    The NdffAPI configuration is read from settings files
    The Datasource configuration is read from settings files
    It reads field-mappings (to map datasource fields to NdffObservation fields)
    and data-mappings (to map data VALUES to Ndff-uri's) from settings files

    """

    # all settings (both main/global ones AND the project/datasource ones)
    # are written in this sub directory
    NDFF_SETTINGS_DIR = 'ndff_settings'

    # global settings
    # settings to connect to api
    NDFF_API_SETTINGS       = 'ndff_api.csv'

    # datasource settings name
    # file name for a settings file containing the type and datasource settings
    NDFF_DATASOURCE_SETTINGS = 'data_source.csv'

    # per project/datasource type settings
    # field/column mappings
    NDFF_OBSERVATION_FIELD_MAPPINGS = 'field_mappings.csv'

    # client settings
    # a file containing information for every NdffObservation field, for example
    # could be used to show a (tranlated) text instead of fieldname. It can also
    # contain the url a client should use to search for a value-uri, a more
    # descriptive text etc etc
    NDFF_OBSERVATION_CLIENT_SETTINGS = 'client_settings.csv'

    EPSG_4326 = 'EPSG:4326'
    EPSG_28992 = 'EPSG:28992'

    DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S'

    # fields in ndff_observation hold a list with:
    # field: text,url1,url2,description,ndff_fieldname
    FIELD_COL_NAME = 0
    FIELD_COL_TEXT = 1
    FIELD_COL_URL1 = 2
    FIELD_COL_URL2 = 3
    FIELD_COL_DESCRIPTION = 4
    FIELD_COL_NDFF_NAME = 5
    FIELD_COL_CHANGE_DATA = 6

    WRONG_FIELD_MAPPING = "VELD NIET BESCHIKBAAR"

    # good enough test for wkt
    # https://regex101.com/
    # currently only "POINT (145918.0769337003 389302.11025674635)" like strings are valid (so UPPERCASE POINT only)
    # OR optional a SRID=4326; in front (EWKT): SRID=4326;POINT (4.67979621887207 51.67397308349609)
    # TODO: QGIS expressions does NOT create POINT but Point (note caps): better to have a more forgiven regexp?
    valid_wkt_point_regex = re.compile(r"(SRID=\d+;)?POINT\s*\(.+\s.+\)", re.MULTILINE | re.UNICODE)
    valid_wkt_multipoint_regex = re.compile(r"(SRID=\d+;)?MULTIPOINT\s*\(.+\s.+\)", re.MULTILINE | re.UNICODE)
    valid_wkt_polygon_regex = re.compile(r"(SRID=\d+;)?POLYGON\s*\(.+\s.+\)", re.MULTILINE | re.UNICODE)


    @staticmethod
    def datetimestring_to_datetime(date_only_or_datetime_string):
        if len(date_only_or_datetime_string.strip()) < 11:
            dt = datetime.strptime(date_only_or_datetime_string, '%Y-%m-%d')
            dt = dt.replace(hour=12, minute=00, second=00)
        elif len(date_only_or_datetime_string.strip()) < 20:
            # 2022-01-01T12:12:00 OR 2022-01-01T12:12:00 both are 'ISO-format' :-(
            dt = datetime.fromisoformat(date_only_or_datetime_string)
        else:
            raise ValueError(f'Trying to create a datetime from a date(time)string which does not to be OK: {date_only_or_datetime_string}')
        return dt

    @staticmethod
    def is_valid_wkt_point(location_string: str) -> bool:
        # 'POINT (145918.0769337003 389302.11025674635)'
        if NdffConnector.valid_wkt_point_regex.match(location_string.upper()):
            return True
        return False

    @staticmethod
    def is_valid_wkt_multipoint(location_string: str) -> bool:
        #
        if NdffConnector.valid_wkt_multipoint_regex.match(location_string.upper()):
            return True
        return False

    @staticmethod
    def is_valid_wkt_polygon(location_string: str) -> bool:
        # POLYGON ((4.41042 51.86444, 4.41042 51.86444, 4.410441 51.86443, 4.41044 51.86444, 4.41042 51.86444))
        if NdffConnector.valid_wkt_polygon_regex.match(location_string.upper()):
            return True
        return False

    @staticmethod
    def read_dict_from_csv(filename: str) -> dict:
        """
        Utility method to read a csv into a dict

        :param filename: full (string) path to csv
        :return: dict
        """
        # TODO: handle absolute and relative paths Note: test/check wel for linux/windows paths!! see:
        # https://stackoverflow.com/questions/3320406/how-to-check-if-a-path-is-absolute-path-or-relative-path-in-a-cross-platform-way
        dictionary = {}
        if (Path(filename)).is_file():
            with open(filename, mode='r', newline='', encoding='utf-8-sig') as f:
                # DictReader, returns a dictionary
                # csv_reader = csv.DictReader(filter(lambda rw: rw[0] != '#', f), delimiter=',', skipinitialspace=True)  # skipping commented lines
                # Normal reader returns one list per row, adding to it based on first column...
                # WHICH IN THIS CASE HAS TO BE UNIQUE !!
                csv_reader = csv.reader(filter(lambda rw: rw[0] != '#', f), delimiter=',', skipinitialspace=True)  # skipping commented lines
                for row in csv_reader:
                    if len(row) == 2:
                        # simple key value pairs
                        dictionary[row[0]] = row[1]
                    elif len(row) > 2:
                        # # rows with more then 2 columns: take the first one as key, others as list:
                        # # row "key,val1,val2" will result in {key:(val1,val2)}
                        # # thinking about using a DictReader here... but ...
                        # if len(row[0]) > 0:  # skipping 'comment rows', being ",,,,,"
                        #     dictionary[row[0]] = row[1:]

                        # rows with more then 2 columns: take the first one as key, full list as value:
                        # row "key,val1,val2" will result in {key:(key, val1,val2)}
                        # thinking about using a DictReader here... but ...
                        if len(row[0]) > 0:  # skipping 'comment rows', being ",,,,,"
                            dictionary[row[0]] = row[0:]
                    else:
                        log.debug(f'Skipping this row in {filename}: "{row}"')
        else:
            pass
            # we deliberately try all files in different dirs...
            # this make is it easier to use this function (instead of checking if something is a file or not)
            #log.warning(f"Filename '{filename}' does not seem to be a file?")
        return dictionary

    @staticmethod
    def create_from_directories(global_config_dir: str, user_config_dir: str, from_within_qgis=False):
        """
        Create a (typed!) Datasource by 'merging' the user-settings/config OVER the
        main/global-settings/config

        :param global_config_dir:
        :param user_config_dir:
        :param from_within_qgis:
        :return:
        """
        # Check if both directories end on DataSource.NDFF_SETTINGS_DIR
        global_config_path = Path(global_config_dir)
        # TODO decide if we also want this one to end on DataSource.NDFF_SETTINGS_DIR:
        # if global_config_path.name != DataSource.NDFF_SETTINGS_DIR:
        #     global_config_path = global_config_path / DataSource.NDFF_SETTINGS_DIR
        user_config_path = Path(user_config_dir)
        if user_config_path.name != NdffConnector.NDFF_SETTINGS_DIR:
            user_config_path = user_config_path / NdffConnector.NDFF_SETTINGS_DIR

        # settings will be a merging of the api_settings AND the datasource_settings
        ndff_api_settings = NdffConnector.read_dict_from_csv(Path(global_config_path) / NdffConnector.NDFF_API_SETTINGS)
        #log.debug(ndff_api_settings)
        user_ndff_api_settings = NdffConnector.read_dict_from_csv(Path(user_config_path) / NdffConnector.NDFF_API_SETTINGS)
        #log.debug(user_api_settings)
        ndff_api_settings.update(user_ndff_api_settings)
        log.debug(ndff_api_settings)

        # ONLY if using the library OUTSIDE of the QGIS plugin, load the datasource settings.
        # IF within QGIS, QGIS/plugin will load the features from the active layer
        datasource_settings = None
        if not from_within_qgis:
            datasource_settings = NdffConnector.read_dict_from_csv(Path(global_config_path) / NdffConnector.NDFF_DATASOURCE_SETTINGS)
            #log.debug(datasource_settings)
            user_datasource_settings = NdffConnector.read_dict_from_csv(Path(user_config_path) / NdffConnector.NDFF_DATASOURCE_SETTINGS)
            #log.debug(user_datasource_settings)
            datasource_settings.update(user_datasource_settings)
            log.debug(datasource_settings)

        # settings will be a merging of the api_settings AND the datasource_settings
        client_settings = NdffConnector.read_dict_from_csv(Path(global_config_path) / NdffConnector.NDFF_OBSERVATION_CLIENT_SETTINGS)
        #log.debug(client_settings)
        user_client_settings = NdffConnector.read_dict_from_csv(Path(user_config_path) / NdffConnector.NDFF_OBSERVATION_CLIENT_SETTINGS)
        #log.debug(client_settings)
        client_settings.update(user_client_settings)
        log.debug(client_settings)

        # load field_mappings and defaults
        field_mappings = NdffConnector.read_dict_from_csv(Path(global_config_path) / NdffConnector.NDFF_OBSERVATION_FIELD_MAPPINGS)
        # NOTE: a the user/project settings should ALWAYS have a field_mappings.csv
        user_field_mappings = NdffConnector.read_dict_from_csv(Path(user_config_path) / NdffConnector.NDFF_OBSERVATION_FIELD_MAPPINGS)
        field_mappings.update(user_field_mappings)
        # extra check, to be sure we only have triplets for every mapping?
        for key, value in field_mappings.items():
            if len(value) != 3:
                raise ValueError(f'Error in field mappings, ALL values should be triplets, but at least one: "{key}" is not a triplet (add a comma to make it one): "{value}"')

        # every field in the NdffObservation has a potential string->ndff-uri DATA mapping file
        # named after the field. Eg for taxon it's file is mapping_taxon.csv
        data_mappings_for_fields = {}
        # create an observation based on master to get the proper fields
        observation = NdffObservation()
        for field in observation.fields():
            filename = f'mappings_{field}.csv'
            data_mappings = NdffConnector.read_dict_from_csv(Path(global_config_path) / filename)
            user_data_mappings = NdffConnector.read_dict_from_csv(Path(user_config_path) / filename)
            data_mappings.update(user_data_mappings)
            data_mappings_for_fields[field] = data_mappings

        # Create the actual connector instance:
        return NdffConnector(ndff_api_settings=ndff_api_settings, datasource_settings=datasource_settings, field_mappings=field_mappings, data_mappings=data_mappings_for_fields, client_settings=client_settings)

    def __init__(self, ndff_api_settings: dict = {}, datasource_settings: dict = {}, field_mappings: dict = {}, data_mappings: dict = {}, client_settings={}):
        self.ndff_api_settings = ndff_api_settings
        self.datasource_settings = datasource_settings
        self.datasource = DataSource.create_from_settings(self.datasource_settings)
        self.data_records = self.datasource.get_records()
        self.field_mappings = field_mappings
        self.data_mappings = data_mappings
        self.client_settings = client_settings
        # NOT going to create an api connection NOW, do it later when somebody requests for a live api connection
        self._api = None

    def next_record(self):
        return next(self.data_records)

    def set_data_records(self, data_records_iterator: iter):
        """
        Normally the specific DataSources will provide data_records
        But in case of QGIS or other clients, it is possible that they provide the
        data theirselves. Giving the option the set the data_records here you can
        still retrieve 'next_record' from this connector
        """
        self.data_records = data_records_iterator

    def get_api(self, fresh_one=False):
        """
        This returns the (or creates an) Api instance from this connector.
        If 'fresh_one' is True then a NEW instance will be created.
        If 'fresh_one' is False (the default), then there will only be created
        a fresh Api instance if there is no one.
        This make is possible to 'invalidate' the api of a connector, for example
        after a ndff_api_settings change, by requesting 'get_api(True)'
        or 'get_api(fresh+one=True)'
        """
        if fresh_one:
            self._api = None
            # and also clean up potentially saved tokens of the old one
            Api.remove_saved_tokens()
        if self._api is None:
            # lazy Api object creation
            self._api = Api(self.ndff_api_settings)
        return self._api

    def get_field_mapping(self, field: str) -> str:
        """
        The connector is responsible for the bookkeeping of the mappings 
        """
        if len(self.field_mappings.keys()) == 0:
            raise Exception('This Connector does not have ANY mappings (from file field_mappings.csv), this should not happen...')
        mapping = None
        if field in self.field_mappings:
            mapping = str(self.field_mappings[field][1]).strip()
            if str(mapping).strip() in ('', '-', 'None'):
                mapping = None
        return mapping

    def set_field_mapping(self, field: str, mapped_field_name) -> bool:
        if len(self.field_mappings.keys()) == 0:
            raise Exception('This Connector does not have ANY mappings (from file field_mappings.csv), this should not happen...')
        if field in self.field_mappings:
            # the value of the field mappings is an immutable tuple as (field, value, default)
            # create a list from it first to be able to edit a value
            updated_mapping = list(self.field_mappings[field])
            updated_mapping[1] = mapped_field_name
            self.field_mappings[field] = tuple(updated_mapping)

    def get_field_default(self, field: str) -> str:
        if len(self.field_mappings.keys()) == 0:
            raise Exception('This Connector does not have ANY mappings (from file field_mappings.csv), this should not happen...')
        default = None
        if field in self.field_mappings:
            default = str(self.field_mappings[field][2]).strip()
            if default and str(default).strip() in ('', '-', 'None'):
                default = None
        return default

    def set_field_default(self, field: str, field_default) -> bool:
        if len(self.field_mappings.keys()) == 0:
            raise Exception('This Connector does not have ANY mappings (from file field_mappings.csv), this should not happen...')
        if field in self.field_mappings:
            # the value of the fieldmappings is a immutable tuple
            # create a list from it
            self.field_mappings[field] = list(self.field_mappings[field])
            self.field_mappings[field][2] = field_default

    def get_field_text(self, field: str) -> str:
        text = field
        if field in self.client_settings.keys():
            text = self.client_settings[field][NdffConnector.FIELD_COL_TEXT]
        return text

    def get_field_ndff_name(self, field: str) -> str:
        ndff_name = field
        if field in self.client_settings.keys():
            ndff_name = self.client_settings[field][NdffConnector.FIELD_COL_NDFF_NAME]
        return ndff_name

    def get_field_description(self, field: str) -> str:
        description = field
        if field in self.client_settings.keys():
            description = self.client_settings[field][NdffConnector.FIELD_COL_DESCRIPTION]
        return description

    def get_field_url1(self, field: str) -> str:
        url1 = field
        if field in self.client_settings.keys():
            url1 = self.client_settings[field][NdffConnector.FIELD_COL_URL1]
        if url1 and str(url1).strip() in ('', '-', 'None'):
            url1 = ''
        return url1

    def get_field_url2(self, field: str) -> str:
        url2 = field
        if field in self.client_settings.keys():
            url2 = self.client_settings[field][NdffConnector.FIELD_COL_URL2]
        if url2 and str(url2).strip() in ('', '-', 'None'):
            url2 = ''
        return url2

    def get_field_change_type(self, field: str) -> str:
        change_type = field
        if field in self.client_settings.keys():
            change_type = self.client_settings[field][NdffConnector.FIELD_COL_CHANGE_DATA]
        return change_type

    def add_extra_info_field_mapping(self, new_identity: str, new_value: str) -> bool:
        """
        The extra_info of an observation comes from a list of key value pairs.
        The key/identity should always be an uri
        The value of it could be an string/number OR uri, BUT always MAPPED
        from the data

        :param new_identity:
        :param new_value:
        :return: True if success else False
        """
        if not is_uri(new_identity):
            log.debug(f'Trying to set an extra info field mapping with an identity which is not an uri: "{new_identity}"')
            return False
        if self.field_mappings and isinstance(self.field_mappings, dict):
            # ugly, just checking highest index
            max_index = 0
            for key in self.field_mappings:
                if key.startswith('extra_info_identity_'):
                    index = int(key[20:])
                    if index > max_index:
                        max_index = index
            # now we found the highest index/runner
            max_index += 1
            self.field_mappings[f'extra_info_identity_{max_index}'] = (f'extra_info_identity_{max_index}', new_identity, None)
            self.field_mappings[f'extra_info_value_{max_index}'] = (f'extra_info_value_{max_index}', new_value, None)
            return True
        else:
            return False

    def delete_extra_info_fiel_mapping (self, field_map_key: str, field_map_value: str) -> bool:
        if field_map_key in self.field_mappings and field_map_value in self.field_mappings:
            self.field_mappings.pop(field_map_key)
            self.field_mappings.pop(field_map_value)
            return True
        return False

    def change_extra_info_field_mapping(self, field_map_key: str, new_identity: str, field_map_value: str, new_value: str) -> bool:
        """
        Change some existing mapping, get it from the live fieldmappings instance
        based on the 'field_map_key' and 'field_map_value', which are the 'keys'
        used in the field_mappings dict, like: extra_info_identity_2 and extra_info_value_2
        :param field_map_key: key like: extra_info_value_2
        :param new_identity: value of the extra info (ndff URI !!!)
        :param field_map_value: key like: extra_info_value_2
        :param new_value: value of extra info (fieldname or value)
        """
        try:
            self.set_field_mapping(field_map_key, new_identity)
            self.set_field_mapping(field_map_value, new_value)
            return True
        except Exception as e:
            #return False # ??
            raise e

    def change_extra_info_field_mapping_values(self, old_identity: str, old_value: str, new_identity: str, new_value: str) -> bool:
        """
        The extra_info of an observation comes from a list of key value pairs.
        Because we do not know if a key of the extra info can be used multiple
        times, we are going to look up from current mappings, so BOTH key(-uri)
        AND value(-mapping)

        Note: it is probably safer to use 'change_extra_info_field_mapping' as
        theoretically an old_identity can be reused in a set of extra info
        (deprecate this one?)

        :param old_identity: actual URI of this extra info
        :param old_value: actual Fieldname (or value) of this extra info
        :param new_identity: URI of new extra info
        :param new_value: new Fieldname (or value) of this extra info
        :return: True if success else False
        """
        # first find the old identity/value in the xtra info mappings
        for key in self.field_mappings:
            if key.startswith('extra_info_identity_'):
                index = int(key[20:])
                value = f'extra_info_value_{index}'
                if self.field_mappings[key][1] == old_identity and self.field_mappings[value][1] == old_value:
                    # replace them with new value, but only if new_identity is also an uri
                    if is_uri(new_identity):
                        self.field_mappings[key] = (key, new_identity, None)
                        self.field_mappings[value] = (value, new_value, None)
                        return True
                    else:
                        log.debug(f'Trying to change an extra info field mapping with an identity which is not an uri: "{new_identity}"')
        log.error(f'Failing to change_extra_info_field_mapping_values: "{old_identity}":"{old_value}" to "{new_identity}":"{new_value}"')
        return False



    def get_data_mapping(self, field: str, field_key: str) -> str:
        """
        Data mappings are dictionaries (in memory AND/OR on disk/in database, depending
        on the type of datasource.

        In current implementation they are saved in the user_settings in a file
        called 'mappings_<field>.csv'

        Not sure yet if we should to lazy loading: as open the file when needed,
        OR early loading: open file and load in memory

        Although 'domain'-tables in databased typically have >2 columns, these
        will be exploded to a long list of key-value pairs...

        Drawback of this implementation: you cannot have the same key for 2
        different uri's. So IF you have
        hop --> plant uri
        you cannot have
        hop -> bird uri
        in the same file...

        You can have the same uri (as value) several times in the mappings:
        for example the nl name, scientific name, an abbreviation, and maybe an
        often made mis-spelling ot the nl name etc etc...

        :param field: the actual field (taxon, activity etc etc)
        :param field_key: (the string which should map to a certain uri)
        :return: field_value: an uri for the field_key or None
        """
        # try to find <field_key' in the mapping dict dict
        # if found return
        # if not found return None
        if field_key in self.data_mappings[field]:
            return self.data_mappings[field][field_key]
        return None

    def set_data_mapping(self, field: str, field_key: str, field_value: str) -> bool:
        """
        Setting a data mapping for given field.
        Both as csv/data/db and in current memory instance of the field
        (self.mappings_<field>

        :param field: the actual field (taxon, activity etc etc)
        :param field_key: (the string which should map to a certain uri)
        :param field_value: an uri for the field_key
        :return: bool True if setting (both in dict and on disk/db) succeeded
                else: False
        """
        # check if field_key is actually a string of length >= 1
        # check if field_value is actually an uri
        if field_key is None or len(field_key) < 1:
            log.error(f'Error: trying to set a data mapping for "{field}" with a field_key "{field_key}" (None or length < 1)')
            return False
        if field_value is None or not is_uri(field_value):
            log.error(f'Error: trying to set a data mapping for "{field}" with a field_value "{field_value}" (None or non-uri)')
            return False

        # check if field_key is already in this dict, if not add it with
        # the corresponding field_value
        if field_key in self.data_mappings[field]:
            ##raise Exception(f'Errr, {field_key} already in mappings for {field}, with value {self.data_mappings[field][field_key]}')
            log.warning(f'WARNING {field_key} already in mappings for {field}, with value {self.data_mappings[field][field_key]} OVERWRITING IT !!!')
        self.data_mappings[field][field_key] = field_value
        return True

    def map_data_to_ndff_observation(self, data_record: dict) -> NdffObservation:
        observation = NdffObservation()
        # creating a location during the ride...?
        # the fields should be filled with actual data, so floats for x, y and buffer and wkt for location
        location_data = {
            'location': None,
            'location_x': None,
            'location_y': None,
            'location_buffer': None
        }
        # go over all fields of the mappings (which contain both the observation
        # fields AND some extra location related fields and see if it is in the data
        for field in self.field_mappings.keys():
            # OK, user SET a field mapping, now check IF this is actually a valid one:
            if field.startswith('extra_info_value'):
                pass  # handled at identity
            elif field.startswith('extra_info_identity'):
                counter = int(field.replace('extra_info_identity_', ''))
                key = self.get_field_mapping(f'extra_info_identity_{counter}')
                if not is_uri(key):
                    log.error(f'Trying to use a non uri key as extra info key: {key}')
                if self.get_field_mapping(f'extra_info_value_{counter}') in data_record:
                    value = data_record[self.get_field_mapping(f'extra_info_value_{counter}')]
                    observation.set_extra_info(key, value)
                else:
                    field = self.get_field_mapping(f'extra_info_value_{counter}')
                    log.error(f'Trying to find a (mapped) field "{field}" in the data.... is it a genuine fieldname?')
            elif self.get_field_mapping(field) in data_record:
                if field in location_data:
                    # handled differently: collect and use later to create location
                    location_data[field] = data_record[self.get_field_mapping(field)]
                else:  # there can be a (faulty) mapping, which is NOT a field in the data
                    observation.set(field, data_record[self.get_field_mapping(field)])
            #else:
                # TOOD: not sure what to do here, set an message so clients can check for that, OR raise an Exception, so mappings will be forced to fit...
                # raise ValueError(f'User set the field mapping of field "{field}" to "{self.get_field_mapping(field)}" but that field is NOT available in the data: {data_record}')
                #log.error(f'User set the field mapping of field "{field}" to "{self.get_field_mapping(field)}" but that field is NOT available in the data')
                #observation.set(field, self.WRONG_FIELD_MAPPING)

        # look for defined default values:
        # set the observation field to default IF it is either None (?OR it was missing?)
        for field in self.field_mappings.keys():
            # location_buffer is a special case: should not be available in the NdffObservation,
            # BUT is needed for a valid geometry, so should be either a mapped value (OR a default)
            # BUT we are only using the default value if it is not set by data from the record yet:
            if field == 'location_buffer' and location_data['location_buffer'] is None:
                location_data[field] = self.get_field_default(field)
            elif field in location_data:
                pass
            elif observation.get(field) is None and self.get_field_default(field):
                observation.set(field, self.get_field_default(field))
            else:
                # TODO log or raise exception?
                pass

        # fixing the location now, either it is filled with a dict or wkt (that is there was a 'location' field)
        # OR location is still None, but x_y_location is filled during this ride...
        log.debug(f'Before create_geom: location_data = {location_data}')
        if self.create_geom(observation, location_data):
            log.debug('Succesfully created a location object')
        else:
            log.debug('NOT created a location object')

        # now go over DATA mappings for every observation field
        for field in observation.fields():
            # check IF there are mappings for this field...
            if field in self.data_mappings.keys():
                # if the value in current observation FIElD is in the data_mappings (as key)
                # (they map from a term/abbreviation/name/id to an uri):
                if (isinstance(observation.get(field), str) or isinstance(observation.get(field), int)) and observation.get(field) in self.data_mappings[field]:
                    # 'overwrite' the value with the 'mapped' value
                    observation.set(field, self.data_mappings[field][observation.get(field)])

        # fix/check period
        result = NdffConnector.create_fix_period(observation)
        if result[0]:
            log.debug('Succesfully created a period for the observation')
        else:
            log.debug(f'NOT created a period for the observation: {result[1]}')

        return observation

    @staticmethod
    def create_fix_period(observation):
        # period_start and period_stop
        if observation.period_start is None and observation.period_stop is None:
            # mmm, apparently nothing is set... non valid record ?
            return False, False
        try:
            # only a period_start is set: add one minute to it and make that period_stop
            if observation.period_start and observation.period_stop is None:
                start = NdffConnector.datetimestring_to_datetime(observation.period_start)
                stop = start + timedelta(minutes=1)
            # only a period_end is set: substract one minute to it and make that period_start
            elif observation.period_stop and observation.period_start is None:
                stop = NdffConnector.datetimestring_to_datetime(observation.period_stop)
                # substract one minute
                start = stop - timedelta(minutes=1)
            else:
                start = NdffConnector.datetimestring_to_datetime(observation.period_start)
                stop = NdffConnector.datetimestring_to_datetime(observation.period_stop)
            # Ok, we should have a valid start AND end now...:
            observation.period_start = start.isoformat()
            observation.period_stop = stop.isoformat()
        except ValueError as v:
            return False, v
        return True, True

    @staticmethod
    def create_geom(observation, location_data):
        """
        Create a location dict from a location_data dict
        The location_data dict is a dict containing 4 keys:
        location, location_x, location_y and location_buffer
        We try to create a valid location-dict as below:

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
        if isinstance(location_data['location'], dict):
            # ok apparently the data is already a dict...
            # this dict should have a buffer already, but if not see if it was in the data
            observation.location = location_data['location']
        else:
            # going to create the geometry dict here ourselves
            # check if we have a x/y or a wkt geom
            if isinstance(location_data['location'], str):
                # can be WKT or EWKT
                # BUT Shapely can ONLY load a WKT string
                # so remove the SRID=28992; part from it in case of EWKT
                if 'SRID' in location_data['location']:
                    location_data['location'] = location_data['location'].split(';')[1]
                try:
                    shapely_geom = shapely.wkt.loads(location_data['location'])
                    if shapely_geom.is_valid:
                        if shapely_geom.geometryType() == 'Point':
                            pass  # all OK
                        elif shapely_geom.geometryType() == 'MultiPoint':
                            # OK we have a multipoint, ONLY using the first one here
                            # as we think that most people will have multipoint data actually mean singlepoint
                            log.debug(f'Location is MultiPoint (according to shapely) BUT we only take the first one!!!')
                            shapely_geom = shapely_geom.geoms[0]
                        else:
                            raise ValueError('Non valid point geometry')
                        observation.location = {'geometry': {}}
                        observation.location['geometry']['type'] = 'Point'
                        observation.location['geometry']['coordinates'] = [float(shapely_geom.x), float(shapely_geom.y)]
                    else:
                        raise ValueError('Non valid geometry')
                except Exception as e:
                    log.debug(f'Error (shapely) creating a geometry from {location_data["location"]}: {e}')
                    return False
            elif location_data['location_x'] is not None and location_data['location_y'] is not None:
                # ok we have an x and y column here...
                observation.location = {'geometry': {}}
                observation.location['geometry']['type'] = 'Point'
                try:
                    observation.location['geometry']['coordinates'] = [float(location_data['location_x']), float(location_data['location_y'])]
                except Exception as e:
                    log.error(f'Error creating a geometry from "{location_data["location_x"]}" and "{location_data["location_y"]}": {e}')
                    return False
            else:
                log.debug('(Yet) unknown geometry type in your wkt...')
                return False

        if 'location_buffer' in location_data and location_data['location_buffer']:
            observation.location['buffer'] = location_data['location_buffer']

        if observation.location and 'geometry' in observation.location and 'coordinates' in observation.location['geometry']:
            # ok we have a geometry with coordinates....
            # TODO fix the crs needed for the api to set the crs header
            #self._set_crs(observation.location['geometry']['coordinates'])
            # all well, return True
            return True

        return False

    def get_crs(self, observation: NdffObservation):
        # "location": {
        #     "buffer": 5,
        #     "geometry": {
        #         "type": "Point",
        #         "coordinates": [
        #             408241,
        #             78648
        #             ]
        #         }
        #     }
        crs = self.EPSG_4326
        location = observation.location
        if location is not None and isinstance(location, dict):
            if 'geometry' in location and location['geometry'] and 'coordinates' in location['geometry']:
                coordinates = location['geometry']['coordinates']
                if float(max(coordinates)) < 200:
                    crs = self.EPSG_4326
                elif float(max(coordinates)) < 620000:
                    crs = self.EPSG_28992
                else:
                    raise ValueError("Coordinates outside of EPSG:4326 or EPSG:28992 range")
        return crs

    def next_ndff_observation(self):
        record = self.next_record()
        return self.map_data_to_ndff_observation(record)

    def __repr__(self):
        return f"""Connector: datasource type: {type(self.datasource)}
ndff_api_settings: {self.ndff_api_settings}
field_mappings: {self.field_mappings}
data_mappings: {self.data_mappings}
"""

    def save_to_directory(self, ndff_config_directory: str, from_within_qgis=False):
        """
        Write current configuration to a directory 'ndff_settings' IN the
        ndff_config_directory given as first parameter

        :param ndff_config_directory: directory to use to create a dir 'ndff_settings'
        and write all params in it
        :param from_within_qgis: if this is written from within the QGIS plugin, we
        are NOT writing the data_source settings (as data is loaded from QGIS layers)
        :return:
        """
        try:
            # write all needed files to this ndff_config_directory
            path = Path(ndff_config_directory)
            # check IF there is already Datasource.NDFF_SETTINGS_DIR ending
            if path.name != DataSource.NDFF_SETTINGS_DIR:
                ndff_config_directory = path / DataSource.NDFF_SETTINGS_DIR
            if not ndff_config_directory.is_dir():
                ndff_config_directory.mkdir(parents=True)
            timestamp = datetime.now().replace(microsecond=0).isoformat()
            if not from_within_qgis:
                self.write_datasource_settings(ndff_config_directory, timestamp)
            self.write_field_mappings(ndff_config_directory, timestamp)
            self.write_data_mappings(ndff_config_directory, timestamp)
        except Exception as e:
            log.error(f'Error saving these NDFF Settings to this directory: {ndff_config_directory}')
            return False
        return True

    def write_datasource_settings(self, ndff_config_directory: str, timestamp: str):
        with open(Path(ndff_config_directory) / self.NDFF_DATASOURCE_SETTINGS, mode='w+', encoding='UTF8', newline='') as f:  # using 'with open', then file is explicitly closed
            writer = csv.writer(f)
            writer.writerow(['#'])
            writer.writerow([f'# This Datasource settings file is written on {timestamp} using the NDFF-Connector'])
            writer.writerow(['#'])
            for key, value in self.datasource_settings.items():
                writer.writerow([key, value])

    def write_field_mappings(self, ndff_config_directory: str, timestamp: str):
        with open(Path(ndff_config_directory) / self.NDFF_OBSERVATION_FIELD_MAPPINGS, 'w+', encoding='UTF8', newline='') as f:  # using 'with open', then file is explicitly closed
            writer = csv.writer(f)
            writer.writerow(['#'])
            writer.writerow([f'# this Field mapping file is written on {timestamp} using the NDFF-Connector'])
            writer.writerow(['#'])
            #for key, value in self.field_mappings.items():
            #    writer.writerow(value)
            # splitting the extra_info key/values from the rest (and TODO also the involved_persons)
            normals = dict(filter(lambda elem: 'extra_info_' not in elem[0], self.field_mappings.items()))
            for key, value in normals.items():
                writer.writerow(value)
            extra_infos = dict(filter(lambda elem: 'extra_info_' in elem[0], self.field_mappings.items()))
            # we are going to rewrite the index/numbers of the extra info's independent of current values
            index = 1  # base 1
            for key in extra_infos:
                if 'extra_info_identity_' in key:
                    counter = int(key.replace('extra_info_identity_', ''))
                    if f'extra_info_identity_{counter}' in extra_infos:
                        key_row   = list(extra_infos[f'extra_info_identity_{counter}'])
                        value_row = list(extra_infos[f'extra_info_value_{counter}'])
                        # recounting/mapping:
                        key_row[0] = key_row[0].replace(str(counter), str(index))
                        value_row[0] = value_row[0].replace(str(counter), str(index))
                        writer.writerow(key_row)
                        writer.writerow(value_row)
                        index += 1
                    else:
                        raise ValueError(f'extra_info_identity_{counter} does not have a coresponding extra_info_value_{counter}.. in the fieldmappings:\n{self.field_mappings}')

            #print(extra_infos)

    def write_data_mappings(self, ndff_config_directory: str, timestamp: str):
        """
        A datasource has a member 'data_mappings' which is a dict of dicts where
        the first one has the field name as key , and a string -> uri mapping as value

        {
         'taxon':             {'Leucojum aestivum': 'http://ndff-ecogrid.nl/taxonomy/taxa/leucojumaestivum', ...},
         'abundance_schema':  {'Exact aantal': 'http://ndff-ecogrid.nl/codes/scales/exact_count', ...},
        }

        The data mappings are written PER FIELD as a csv with name mappings_<fieldname>.csv
        so for example for taxon: mappings_taxon.csv
        """
        for field in self.data_mappings.keys():
            # BUT only if there ARE actually mappings
            if len(self.data_mappings[field]) > 0:
                with open(Path(ndff_config_directory) / f'mappings_{field}.csv', 'w+', encoding='UTF8', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(['#'])
                    writer.writerow([f'# this Data mapping file for {field} is written {timestamp} using the NDFF-Connector'])
                    writer.writerow(['#'])
                    for key, value in self.data_mappings[field].items():
                        writer.writerow([key, value])
