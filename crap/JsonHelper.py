import json
import os.path


class JsonHelper:
    file_reference: str
    data_tracker: dict = None

    def __init__(self, file_ref: str):
        self.file_reference = file_ref

    def get_dict(self) -> dict:
        return json.load(open(self.file_reference, "r", encoding='utf-8'))

    def replace_data(self, new_dict) -> None:
        json.dump(new_dict, open(self.file_reference, "w", encoding='utf-8'))

    def ensured_key(self, key: str, replacement=None):
        """
        Ensures that if the key isn't found it will have a replacement

        :param key: The key to look for.
        :param replacement: The replacement data if 'key' isn't found
        """

        json_object = self.get_dict()
        if key in json_object.keys():
            return json_object[key]
        else:
            return replacement

    def safe_ensured_key(self, key: str, replacement=None):
        """
        Ensures that if the key isn't found it will have a replacement but uses memory rather than opening a file everytime

        :param key: The key to look for.
        :param replacement: The replacement data if 'key' isn't found
        """

        if not self.data_tracker:
            self.data_tracker = self.get_dict()

        if key in self.data_tracker.keys():
            return self.data_tracker[key]
        else:
            return replacement

    def end_data_tracking(self):
        del self.data_tracker

    @staticmethod
    def conditional_init(file_ref: str):
        if os.path.exists(file_ref):
            return JsonHelper(file_ref)
