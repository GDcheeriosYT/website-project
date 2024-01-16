import os

from .Account import Account


class AccountList:
    def __init__(self):
        print("Loading account data")

        self.accounts = []
        for account in os.listdir("accounts"):
            self.accounts.append(Account(account[:-5]))
