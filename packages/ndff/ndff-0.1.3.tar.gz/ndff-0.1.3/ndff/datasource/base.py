import logging
from pathlib import Path
import csv
log = logging.getLogger(__name__)

class DataSource:
    """
    A DataSource is a class which (using the information from the config directories)
    is able to load / connect to a Datasource and can hand over NdffObservation
    objects one by one, either as an iterator, OR based on ID

    Via the datasource you also configure the logging.
    Can be to a separate log table in a database
    Can be a separate csv/txt file
    Can maybe also be changing the input file by filling certain columns?
    """

    # all settings (both main/global ones AND the project/datasource ones)
    # are written in this sub dir
    NDFF_SETTINGS_DIR = 'ndff_settings'

    # global settings
    # settings to connect to api
    NDFF_API_SETTINGS       = 'ndff_api.csv'
    # default fields and names
    NDFF_OBSERVATION_FIElDS = 'ndff_observation.csv'

    # per project/datasource type settings
    # field/column mappings
    NDFF_OBSERVATION_FIELD_MAPPINGS = 'field_mappings.csv'
    # field/column defaults
    # TODO figure out if we want this to be a separate file...
    NDFF_OBSERVATION_FIELD_DEFAULTS = 'field_defaults.csv'
    # datasource settings
    NDFF_DATASOURCE_SETTINGS = 'data_source.csv'

    @staticmethod
    def create_from_settings(settings={}):
        # type of DataSource in in settings:
        if settings and 'datasource_type' in settings:
            if settings['datasource_type'] == 'postgres':
                from .postgres import PostgresDataSource
                ds = PostgresDataSource(settings)
            elif settings['datasource_type'] == 'csv':
                from .csv import CsvDataSource
                ds = CsvDataSource(settings)
            # elif settings['datasource_type'] == 'qgis':
            #     ds = QgisDataSource(settings)
            else:
                raise Exception(f"Not Yet Implemented DataSource type: {settings['datasource_type']}")
        else:
            ds = DataSource(settings)
        ds.settings = settings
        return ds

    def __init__(self, settings={}):
        self.settings = settings
        self.ndff_config_directory = None  # NOT YET DEFINED...

    def __repr__(self):
            return f"""Datasource: {self.__class__} {type(self)}
settings: {self.settings}
"""

    def _set_settings(self):
        '''
        To set type depending properties based on the self.settings.
        To be implemented by subtypes
        '''
        pass

    def get_records(self, working_dir=Path('.')):
        #log.warning(f'Not Implemented: "get_records" should be implemented in {self.__class__}')
        for record in []:
            yield record

    def get_record_by_id(self, id=None, id_name='id'):
        log.critical(f'Not Implemented: "get_records" should be implemented in {self.__class__}')
        return []
