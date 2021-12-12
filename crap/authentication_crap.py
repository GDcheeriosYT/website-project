#securing / importing flask variables
import Client_Credentials as client

#packages
import requests
import time

def client_grant():
    global response
    print("granting client...")
    response = requests.post(f"https://osu.ppy.sh/oauth/token", headers = {"Accept": "application/json", "Content-Type": "application/json"}, json = {"client_id": client.client_id, "client_secret": f"{client.secret}", "grant_type": "client_credentials", "scope": "public"}).json()
    print("client succsefully granted!")
    return(response["access_token"])