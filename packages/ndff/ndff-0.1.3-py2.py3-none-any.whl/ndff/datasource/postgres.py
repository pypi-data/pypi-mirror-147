import logging
from .base import DataSource
import psycopg2
from psycopg2.extras import DictCursor
from pathlib import Path

log = logging.getLogger(__name__)


class PostgresDataSource(DataSource):

    def __init__(self, settings={}):
        super().__init__(settings)
        log.debug(f'Init PostgresDataSource, settings: {self.settings}')
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.dbname = None
        self.timeout = None
        self.table = None
        self._set_settings()

    def _set_settings(self):
        if 'postgres_host' in self.settings:
            self.host = self.settings['postgres_host']
        if 'postgres_port' in self.settings:
            self.port = self.settings['postgres_port']
        if 'postgres_user' in self.settings:
            self.user = self.settings['postgres_user']
        if 'postgres_password' in self.settings:
            self.password = self.settings['postgres_password']
        if 'postgres_dbname' in self.settings:
            self.dbname = self.settings['postgres_dbname']
        if 'postgres_timeout' in self.settings:
            self.timeout = self.settings['postgres_timeout']
        if 'postgres_table' in self.settings:
            self.table = self.settings['postgres_table']

        # only if seemingly valid host and user etc:
        if self.host is not None and self.user is not None and self.dbname is not None:
            try:
                self.conn = psycopg2.connect(
                                host=self.host,
                                port=self.port,
                                user=self.user,
                                password=self.password,
                                dbname=self.dbname,
                                connect_timeout=self.timeout)
            except:
                log.error('Unable to connect to {} database using "{}@{}:{}" within {} seconds'.format(self.host, self.user, self.dbname, self.port, self.timeout))
                raise

    def get_records(self, working_dir=Path('.')):
        """
        https://stackoverflow.com/questions/12379221/sql-query-to-find-primary-key-of-a-table/12379241
        
        SELECT k.COLUMN_NAME
        FROM information_schema.table_constraints t
        LEFT JOIN information_schema.key_column_usage k
        USING(constraint_name,table_schema,table_name)
        WHERE t.constraint_type='PRIMARY KEY'
            AND t.table_schema='schema'
            AND t.table_name='table';
        """
        cur = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        select_query = f'select * from {self.table} order by id'
        cur.execute(select_query)
        return cur.__iter__()

