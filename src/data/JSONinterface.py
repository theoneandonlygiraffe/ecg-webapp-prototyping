import json

class JSONEncodable(object):
    def json(self):
        return vars(self)