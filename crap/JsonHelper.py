import json


class JsonHelper:
    file_reference: str
    data_tracker: dict

    def __init__(self, file_ref: str):
        self.file_reference = file_ref

    def get_dict(self) -> dict:
        return json.load(open(self.file_reference, "r", encoding='utf-8'))

    def replace_data(self, new_dict) -> None:
        json.dump(new_dict, open(self.file_reference, "w", encoding='utf-8'))

    def assured_key(self, key: str, replacement=None):
        json_object = self.get_dict()
        if key in json_object.keys():
            return json_object[key]
        else:
            return replacement

    def safe_assured_key(self, key: str, replacement=None):
        if self.data_tracker:
            json_object = self.data_tracker
        else:
            json_object = self.get_dict()

        if key in json_object.keys():
            return json_object[key]
        else:
            return replacement

    def end_data_tracking(self):
        del self.data_tracker
