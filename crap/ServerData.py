from crap.ApiCall import ApiCall
from crap.ApiType import ApiType


class ServerData:
    API_history = []

    @staticmethod
    def api_call(type: ApiType):
        api_call = ApiCall(type)
        print(f"handling Api call {api_call.id} [{api_call.type}]")
        ServerData.API_history.append(api_call)
