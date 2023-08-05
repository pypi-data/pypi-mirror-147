"""
There are 4 type of data:
1. Dataframe
2. List of json
3. List
4. Value
"""
import json
import re

import pandas as pd
import numpy as np


class Cleansing:
    def __init__(self, data: pd.DataFrame, column: str, param: json):
        try:
            self.data = data
        except KeyError:
            raise KeyError

        param_key = param.keys()

        if 'type_value' in param_key:
            mapping = {"float": float, "int": "Int64", "str": str}
            type_value = param['type_value']
            print('clean {} {} {}'.format(column, 'type_value', str(type_value)))
            self.data[column] = self.data[column].apply(self.type_value, key=type_value)

            print('convert {} {} {}'.format(column, 'type_value', str(mapping[type_value])))
            self.data[column] = self.data[column].astype(mapping[type_value])

        if 'non_endswith_value' in param_key:
            non_endswith_value = param['non_endswith_value']
            print('clean {} {} {}'.format(column, 'non_endswith_value', str(non_endswith_value)))
            self.data[column] = self.data[column].apply(self.non_endswith_value, key=non_endswith_value)

        if 'min_length_value' in param_key:
            min_length_value = param['min_length_value']
            print('clean {} {} {}'.format(column, 'min_length_value', str(min_length_value)))
            self.data[column] = self.data[column].apply(self.min_length_value, key=min_length_value)

        if 'max_length_value' in param_key:
            max_length_value = param['max_length_value']
            print('clean {} {} {}'.format(column, 'max_length_value', str(max_length_value)))
            self.data[column] = self.data[column].apply(self.max_length_value, key=max_length_value)

        if 'non_empty_value' in param_key:
            if param['non_empty_value'] is True:
                print('clean {} {}'.format(column, 'non_empty_value'))
                self.data = self.data.dropna(subset=[column])

    @staticmethod
    def type_value(val, key: str):
        if not pd.isnull(val):
            mapping = {"float": float, "int": int, "str": str, "list": list}
            number = [float, int]
            if key not in mapping.keys():
                raise KeyError

            key = mapping[key]

            if isinstance(val, key):
                pass
            else:
                if key in number:
                    val = remove_non_number(val, key)
                    if val is np.nan:
                        return val

                try:
                    val = key(val)
                except ValueError:
                    val = np.nan
        return val

    @staticmethod
    def max_length_value(val, key: int):
        if not pd.isnull(val):
            value = str(val)
            if len(value) > key:
                val = None
            else:
                pass
        return val

    @staticmethod
    def min_length_value(val, key: int):
        if not pd.isnull(val):
            value = str(val)
            if len(value) < key:
                val = None
            else:
                pass
        return val

    @staticmethod
    def max_value(val, key):
        if val > key:
            val = False
        else:
            val = True
        return val

    @staticmethod
    def min_value(val, key):
        if val < key:
            val = False
        else:
            val = True
        return val

    @staticmethod
    def letter_case_value(val, key):
        valid_key = ['upper', 'lower', 'capitalized']
        if key not in valid_key:
            raise ValueError('Key is invalid')

        if key == 'upper':
            if val.isupper():
                val = True
            else:
                val = False
        elif key == 'lower':
            if val.islower():
                val = True
            else:
                val = False
        else:
            list_val = val.split(' ')
            list_val = [True for val in list_val if val[0].isupper()]
            if True in list_val:
                val = True
            else:
                val = False
        return val

    @staticmethod
    def startswith_value(val: str, key: str):
        if val.startswith(key):
            val = True
        else:
            val = False
        return val

    @staticmethod
    def endswith_value(val: str, key: str):
        if val.endswith(key):
            val = True
        else:
            val = False
        return val

    @staticmethod
    def non_startswith_value(val: str, key: str):
        if val.startswith(key):
            val = True
        else:
            val = False
        return val

    @staticmethod
    def non_endswith_value(val, key: str):
        if not pd.isnull(val):
            value = str(val)
            if value.endswith(key):
                val = None
            else:
                pass
        return val


def remove_non_number(val, number_type):
    val = str(val)
    non_decimal = re.compile(r'[^\d.]+')
    val = non_decimal.sub('', val)
    val = val.replace(' ', '')

    if val == '':
        val = np.nan
        return val

    if number_type == int:
        val = val.split('.')[0]

    return val
