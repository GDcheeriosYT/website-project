from enum import Enum, auto


class ApiType(Enum):
    # tokens
    TokenGenerate = auto()
    TokenVerify = auto()
    TokenDelete = auto()
    TokenClear = auto()

    #  accounts
    AccountCreate = auto()
    AccountLogIn = auto()
    AccountLogOut = auto()
    AccountChangePfp = auto()
    AccountReceive = auto()

    # osu
    OsuRefresh = auto()
    OsuAuthenticate = auto()
    OsuMatchGrab = auto()
    OsuLiveUpdate = auto()
    OsuLiveGet = auto()
    OsuLiveDelete = auto()
    OsuIdGrab = auto()

    # gentry quest
    GQCheckIn = auto()
    GQCheckOut = auto()
    GQLeaderboard = auto()
    GQUpdateData = auto()
    GQGetPowerLevel = auto()
    GQGetOnlinePlayers = auto()
    GQGetVersion = auto()
