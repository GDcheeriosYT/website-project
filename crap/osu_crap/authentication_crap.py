# securing / importing flask variables
import Client_Credentials as client

# packages
import requests
import datetime as dt


# osu
def client_grant():
    global access_token
    global expiration
    print("granting client...")
    response = requests.post(f"https://osu.ppy.sh/oauth/token",
                             headers={"Accept": "application/json", "Content-Type": "application/json"},
                             json={"client_id": client.osu_client_id, "client_secret": f"{client.osu_secret}",
                                   "grant_type": "client_credentials", "scope": "public"}).json()
    print("client succsefully granted!")
    access_token = response["access_token"]
    dt_obj = dt.datetime.now()
    expiration = round(dt_obj.microsecond / 1000) + response["expires_in"]
    return (response["access_token"])


def check_access():
    dt_obj = dt.datetime.now()
    print("checking token expiration...")
    try:
        if round(dt_obj.microsecond / 1000) > expiration:
            client_grant()
        else:
            print("token is valid!")
    except:
        client_grant()
