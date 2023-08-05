import os
from datetime import datetime

from dotenv import load_dotenv
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId


class Connection:
    def __init__(self, source, db_name):
        if source == 'pelaporan':
            load_dotenv()
            self.host = os.environ.get("MONGODB_HOST")
            self.port = os.environ.get("MONGODB_PORT")
            self.database = db_name
        else:
            raise ConnectionError('Connection not found')

        self.url = 'mongodb://{}:{}'.format(self.host, self.port)
        self.client = None
        self.db = None

    def connect(self):
        try:
            self.client = MongoClient(self.url)
            self.db = self.client[self.database]
            print("Connect Client MongoDB")
            return self.client, self.db
        except:
            raise ConnectionError("Connection error")

    def close(self):
        self.client.close()


class Get:
    def __init__(self, source, database):
        self.connection = Connection(source, database)
        self.client = None
        self.db = None
        self.allowed_return_value = ['dataframe', 'json']

        self.client, self.db = self.connection.connect()

    def by_collection(self, collection, return_value, limit=None, last_id=None):
        if return_value not in self.allowed_return_value:
            raise ValueError('return_type value is invalid')

        data = None
        coll = self.db[collection]
        if limit:
            if last_id:
                data = coll.find({'_id': {'$gt': last_id}}).limit(limit)
            else:
                coll.find().limit(limit)
        else:
            data = coll.find()

        data = decode_wrapper(data)

        if return_value == 'dataframe':
            data = pd.DataFrame(data)
        else:
            pass
        return data

    def close(self):
        self.connection.close()


def decode_wrapper(datas):
    if isinstance(datas, list):
        start_length = len(datas)
        list_data = []
        if datas:
            for data in datas:
                if isinstance(data, dict):
                    json_data = {}
                    key_data = data.keys()
                    for key_dat in key_data:
                        dat = data[key_dat]
                        if isinstance(dat, datetime):
                            dat = dat.strftime("%Y-%m-%d %H:%M:%S")
                        elif isinstance(dat, ObjectId):
                            dat = str(dat)
                        elif isinstance(dat, bytes):
                            dat = dat.decode('utf-8')
                        elif isinstance(dat, list):
                            dat = decode_wrapper(dat)
                        json_data.update({key_dat: dat})
                    list_data.append(json_data)
                elif isinstance(data, datetime):
                    data = data.strftime("%Y-%m-%d %H:%M:%S")
                    list_data.append(data)
                elif isinstance(data, ObjectId):
                    data = str(data)
                    list_data.append(data)
                elif isinstance(data, bytes):
                    data = data.decode('utf-8')
                    list_data.append(data)
                elif isinstance(data, list):
                    data = decode_wrapper(data)
                    list_data.append(data)
                else:
                    list_data.append(data)
        datas = list_data
        # evaluate
        end_length = len(datas)
        print("start data length: {}, end data length: {}".format(str(start_length), str(end_length)))
    elif isinstance(datas, datetime):
        datas = datas.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(datas, ObjectId):
        datas = str(datas)
    elif isinstance(datas, bytes):
        datas = datas.decode('utf-8')
    elif isinstance(datas, list):
        datas = decode_wrapper(datas)
    else:
        datas = datas
    return datas
