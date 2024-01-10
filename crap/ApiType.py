from enum import Enum


class ApiType(Enum):

    # tokens
    TokenGenerate = 0
    TokenVerify = 1
    TokenDelete = 2
    TokenClear = 3

    #  accounts
    AccountCreate = 4
    AccountLogIn = 5
    AccountChangePfp = 6

    # osu
    OsuRefresh = 7
    OsuAuthenticate = 8

    # gentry quest
