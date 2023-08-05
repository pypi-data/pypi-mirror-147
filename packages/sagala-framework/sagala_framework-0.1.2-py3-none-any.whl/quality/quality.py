"""
Masih yang hanya untuk dataframe

"""
import json

import pandas as pd


class Completeness:
    def __init__(self, data: pd.DataFrame, column: str, param: json):
        self.result = []
        self.quality_column = {
            'table_name': str,
            'column_name': str,
            'dimension_type': str,
            'metric_type': str,
            'data_value': str,
            'data_count': int,
            'data_percentage': float
        }
        try:
            self.data = data[column]
        except KeyError:
            raise KeyError

        data_length = len(data.index)
        df_base = pd.DataFrame(columns=self.quality_column, data=[[column, 'total', data_length, 100]])
        param_key = param.keys()
        for key in param_key:
            if key == 'non_empty_value':
                result = self.data.apply(self.non_empty_value)
                result = result.value_counts()

                df_non_empty_value = df_base
                df_non_empty_value['column_name'] = column
                df_non_empty_value['completeness_type'] = key
                df_non_empty_value['data_value'] = result.index
                df_non_empty_value['data_count'] = result
                df_non_empty_value['percentage'] = df_non_empty_value['data_count'] / data_length

                df_non_empty_value['data_value'] = df_non_empty_value['data_value'].replace(True, 'non_empty_value')
                df_non_empty_value['data_value'] = df_non_empty_value['data_value'].replace(False, 'empty_value')
                df_non_empty_value = df_non_empty_value.to_records(index=False)
                self.result.append(df_non_empty_value)

    @staticmethod
    def non_empty_value(val):
        if val is None:
            result = False
        elif val == '':
            result = False
        else:
            result = True
        return result

    @staticmethod
    def type_value(val, key, key_format=None):
        if isinstance(val, key):
            result = True
        else:
            try:
                if key == 'integer':
                    val = int(val)
                    result = True
                elif key == 'float':
                    val = float(val)
                    result = True
            except:
                result = False

        return result

    @staticmethod
    def max_length_value(self, val: str, key: int):
        if len(val) > key:
            self.result = False
        else:
            self.result = True
        return self.result

    @staticmethod
    def min_length_value(self, val: str, key: int):
        if len(val) < key:
            self.result = False
        else:
            self.result = True
        return self.result

    @staticmethod
    def max_value(self, val, key):
        if val > key:
            self.result = False
        else:
            self.result = True
        return self.result

    @staticmethod
    def min_value(self, val, key):
        if val < key:
            self.result = False
        else:
            self.result = True
        return self.result

    @staticmethod
    def letter_case_value(self, val, key):
        valid_key = ['upper', 'lower', 'capitalized']
        if key not in valid_key:
            raise ValueError('Key is invalid')

        if key == 'upper':
            if val.isupper():
                self.result = True
            else:
                self.result = False
        elif key == 'lower':
            if val.islower():
                self.result = True
            else:
                self.result = False
        else:
            list_val = val.split(' ')
            list_val = [True for val in list_val if val[0].isupper()]
            if True in list_val:
                self.result = True
            else:
                self.result = False
        return self.result

    @staticmethod
    def startswith_value(self, val: str, key: str):
        if val.startswith(key):
            self.result = True
        else:
            self.result = False
        return self.result

    @staticmethod
    def endswith_value(self, val: str, key: str):
        if val.endswith(key):
            self.result = True
        else:
            self.result = False
        return self.result

    @staticmethod
    def non_startswith_value(self, val: str, key: str):
        if val.startswith(key):
            self.result = False
        else:
            self.result = True
        return self.result

    @staticmethod
    def non_endswith_value(self, val: str, key: str):
        if val.endswith(key):
            self.result = False
        else:
            self.result = True
        return self.result


class Freshness:
    # cek kapan terakhir data diupdate, cek dari metadata
    @staticmethod
    def table_freshness(schema, table):
        last_update = ''
        return last_update

    @staticmethod
    def column_freshness(schema, table, column):
        last_update = ''
        return last_update


class Uniqueness:
    def __init__(self):
        pass

    def distinct(self):
        pass


class Consistency:
    def same_length(self):
        pass

    def same_value(self):
        pass

    def same_start(self):
        pass

    def same_end(self):
        pass


# belum dipake
class Usability:
    # cek penggunaan data
    pass
