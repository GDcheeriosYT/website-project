import json

from crap.Event import Event
from crap.ApiCall import ApiCall
from crap.ApiType import ApiType
from crap.AccountList import AccountList
from crap.StatusHandler import StatusHandler


class ServerData:
    # main data
    account_manager = AccountList()
    tokens = []

    # osu
    osu_player_json = json.load(open("player_data.json"))

    # api
    API_history = []
    API_rate_hour = 0
    API_rate_minute = 0
    API_rate_second = 0
    API_total_second = 0
    API_most_common = None
    API_occurrences = {}
    for type in ApiType:
        API_occurrences[str(type.value)] = 0

    # status
    token_status = StatusHandler("token")
    account_status = StatusHandler("account")
    osu_status = StatusHandler("osu")
    gqc_status = StatusHandler("Gentry's Quest Classic")
    gq_status = StatusHandler("Gentry's Quest")

    # events
    on_api = Event("OnApi")

    @staticmethod
    def api_call(type: ApiType) -> None:
        api_call = ApiCall(type)
        print(f"handling Api call {api_call.id} [{api_call.type}]")
        ServerData.API_history.append(api_call)
        type = str(api_call.type.value)
        ServerData.API_occurrences[type] += 1

        current = api_call.timestamp.now()
        # ServerData.API_rate_hour = int((len(ServerData.API_history) / (current.second / 3600)))
        # ServerData.API_rate_minute = int((len(ServerData.API_history) / (current.second / 60)))
        # ServerData.API_rate_second = int((len(ServerData.API_history) / current.second))
        ServerData.on_api()

    @staticmethod
    def get_occurrences():
        return {
            'names': [ApiType(int(type_str)).name for type_str in ServerData.API_occurrences.keys()],
            'values': [ServerData.API_occurrences.get(type_str) for type_str in ServerData.API_occurrences.keys()]
        }

    @staticmethod
    def add_token(token: str) -> None:
        # Api call here is unnecessary
        ServerData.tokens.append(token)

    @staticmethod
    def clear_tokens() -> None:
        ServerData.api_call(ApiType.TokenClear)
        ServerData.tokens = []

    @staticmethod
    def remove_token(token: str) -> None:
        ServerData.api_call(ApiType.TokenDelete)
        try:
            ServerData.tokens.remove(token)
            ServerData.token_status.successful()
        except:
            ServerData.token_status.unsuccessful()

    @staticmethod
    def verify_token(token: str) -> str:
        ServerData.api_call(ApiType.TokenVerify)
        try:
            return token
        except:
            ServerData.token_status.unsuccessful()
            return "False"
