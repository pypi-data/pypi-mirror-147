import json


class Completeness:
    def __init__(self):
        pass

    @staticmethod
    def nik():
        with open('metadata/quality/nik.json') as f:
            data = json.load(f)
        return data
