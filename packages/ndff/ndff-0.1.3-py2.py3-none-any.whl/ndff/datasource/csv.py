import logging
import csv
from .base import DataSource
from pathlib import Path

log = logging.getLogger(__name__)

class CsvDataSource(DataSource):

    def __init__(self, settings={}):
        super().__init__(settings)
        log.debug(f'Init CsvDataSource, settings: {self.settings}')
        self.file = None
        self.csv_file = None
        self.csv_reader = None
        self.delimiter = ','
        self._set_settings()

    def get_records(self):
        log.debug(f'Reading records from: {self.file}')
        with open(self.file, newline='', mode='r', encoding='utf-8-sig') as self.csv_file:
            # Normal reader, returns a list of every row
            # csv_reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            # DictReader, returns a dictionary
            self.csv_reader = csv.DictReader(self.csv_file, delimiter=self.delimiter, skipinitialspace=True)
            for row in self.csv_reader:
                #print(f'{type(row)} {row}')
                yield row

    def _set_settings(self):
        if 'csv_file' in self.settings:
            self.file = self.settings['csv_file']
        if 'csv_delimiter' in self.settings:
            self.delimiter = self.settings['csv_delimiter']
