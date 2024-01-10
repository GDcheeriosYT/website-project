import datetime as dt

from crap.ApiType import ApiType


class ApiCall:
    counter = 0

    def __init__(self, type: ApiType):
        self.id = ApiCall.counter
        ApiCall.counter += 1

        self.type = type

        self.timestamp = dt.datetime.now()
