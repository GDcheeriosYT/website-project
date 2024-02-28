import datetime as dt
import os
import shutil


def create_backup():
    current = dt.datetime.now()
    current = f"{current.date()} {current.hour}{current.minute}{current.second}"
    print(f"making backup for {current}")

    os.mkdir(f"backups/{current}")
    shutil.copytree("accounts", f"backups/{current}/accounts")
    shutil.copytree("matches", f"backups/{current}/matches")
    shutil.copytree("match_history", f"backups/{current}/match_history")
