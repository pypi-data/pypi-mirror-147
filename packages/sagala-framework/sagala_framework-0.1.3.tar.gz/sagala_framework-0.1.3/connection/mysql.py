import os
from os.path import join, dirname

from dotenv import load_dotenv
import pymysql
from sqlalchemy import create_engine
import pandas as pd


class Connection:
    def __init__(self, source, db_name):
        __file__ = 'connection/'
        dotenv_path = join(dirname(__file__), 'connection.env')
        # dotenv_path = 'connection.env'
        load_dotenv(dotenv_path)

        self.username = os.environ.get("MYSQL_{}_USERNAME".format(source))
        self.password = os.environ.get("MYSQL_{}_PASSWORD".format(source))
        self.host = os.environ.get("MYSQL_{}_HOST".format(source))
        self.port = os.environ.get("MYSQL_{}_PORT".format(source))
        self.database = db_name
        self.engine = None
        self.engine_conn = None
        self.conn = None
        self.cursor = None

    def connection(self, conn_type):
        if conn_type == 'engine':
            self.engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'
                                        .format(self.username, self.password, self.host, self.port, self.database))
            self.engine_conn = self.engine.connect()
            print("Connect Engine MySQL")
            return self.engine, self.engine_conn
        else:
            print("No Connection")

    def close(self):
        if self.engine:
            self.engine_conn.close()
            self.engine.dispose()
        if self.conn:
            self.cursor.close()
            self.conn.close()


class Get:
    def __init__(self, source, database):
        self.connection = Connection(source, database)
        self.engine = None
        self.conn = None
        self.allowed_return_value = ['dataframe', 'json']

        try:
            self.engine, self.conn = self.connection.connection('engine')
        except:
            raise ConnectionError('Connection error')

    def by_query(self, query, return_value):
        if return_value not in self.allowed_return_value:
            raise ValueError('return_type value is invalid')

        data = pd.read_sql_query(con=self.conn, sql=query)
        if return_value == 'dataframe':
            pass
        else:
            data = data.to_records(index=False)
        return data

    def by_table(self, table, return_value):
        if return_value not in self.allowed_return_value:
            raise ValueError('return_type value is invalid')

        data = pd.read_sql_table(con=self.conn, table_name=table)
        if return_value == 'dataframe':
            pass
        else:
            data = data.to_records(index=False)
        return data

    def close(self):
        self.connection.close()


class Post:
    a = ''
