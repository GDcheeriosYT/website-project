#securing / importing flask variables
import Client_Credentials as client

#packages
import requests
import time

async def client_grant_loop():
    global response
    while True:
        print("granting client")
        response = requests.post(f"https://osu.ppy.sh/oauth/token", headers = {"Accept": "application/json", "Content-Type": "application/json",}, body = {"client_id": client.client_id, "client_secret": f"{client.secret}", "grant_type": "client_credentials", "scope": "public"}).json()
        print(response)
        time.sleep(86100)

def get_access_token():
    return response