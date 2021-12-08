import urllib.request
import Client_Credentials as client
import time
import datetime as dt

while True:
  print("making a request to authenticate")
  page = urllib.request.urlopen(f'{client.public_url}/benis')
  page.close()
  time.sleep(86100)