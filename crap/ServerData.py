from crap.ApiCall import ApiCall
from crap.ApiType import ApiType
from crap.AccountList import AccountList


class ServerData:
    accounts = AccountList()
    tokens = []

    API_history = []

    @staticmethod
    def api_call(type: ApiType) -> None:
        api_call = ApiCall(type)
        print(f"handling Api call {api_call.id} [{api_call.type}]")
        ServerData.API_history.append(api_call)

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
        ServerData.tokens.remove(token)

    @staticmethod
    def verify_token(token: str) -> str:
        ServerData.api_call(ApiType.TokenVerify)
        return token if token in ServerData.tokens else None
