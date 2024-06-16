import os
import time
import json

import Client_Credentials

from .Account import Account


class AccountList:
    def __init__(self):
        print("\nLoading account data\n")
        time.sleep(Client_Credentials.section_load_time)

        self.accounts = []
        for account in os.listdir("accounts"):
            self.accounts.append(Account(account))
            time.sleep(Client_Credentials.load_time)

    def unload(self):
        for account in self.accounts:
            with open(f"accounts/{account.id}/data.json", "w") as account_file:
                json.dump(account.jsonify(), account_file, indent=4)

    def get_by_id(self, id) -> Account:
        for account in self.accounts:
            account_id = str(account.id)
            id = str(id)
            if account_id == id:
                return account

    def get_by_username(self, username):
        for account in self.accounts:
            if account.username == username:
                return account

    def has_permission(self, id, permission: str):
        if id:
            perms = self.get_by_id(id).perms
            if perms:
                return permission in perms

        return False

    def make_account(self, id):
        self.accounts.append(Account(id))

    def size(self) -> int:
        return len(self.accounts)
