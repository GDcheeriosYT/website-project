import os
from dotenv import load_dotenv

load_dotenv()

# main variables
domain = os.environ['DOMAIN']
port = os.environ['PORT']  # the port
debug = False  # debugging?
secret = os.environ['SECRET']

# DB
db_user = os.environ['DB_USER']
db_password = os.environ['DB_PASSWORD']
db_hostname = os.environ['DB_HOSTNAME']
db_port = os.environ['DB_PORT']
db = os.environ['DB']

# osu
osu_secret = os.environ['OSU_SECRET']
osu_api_key = os.environ['OSU_API_KEY']
osu_client_id = os.environ['CLIENT_ID']
