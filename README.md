# website-project
A multi purpose project using flask for my own api and website
http://gdcheerios.com

If you wanna start your own instance make sure to make a file called Client_Credentials.py with the following structure:

```py
# main variables
domain = "https://mydomain.com"
port = "80"  # the port
load_time = 0  # extra delay for loading iterations in seconds
section_load_time = 0  # extra delay for each loading section in seconds
debug = False  # debugging?
gq_rating = False  # rating gentry's quest?

# ssl
cert_path = None  # the path for the cert.pem
key_path = None  # the path for the key.pem

# osu
osu_secret = "blahblahblahblah" # client secret
osu_api_key = "a1b2c3etc" # api key
osu_client_id = "1234" # client id
```
