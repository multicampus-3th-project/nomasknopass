import sys
import requests

URL = 'http://3.35.94.100:8000/mask/'
# r = requests.get('http://3.35.94.100:8000/mask/')

client = requests.session()

# Retrieve the CSRF token first
client.get(URL)  # sets cookie
if 'csrftoken' in client.cookies:
    # Django 1.6 and up
    csrftoken = client.cookies['csrftoken']
    # print(csrftoken)
else:
    # older versions
    csrftoken = client.cookies['csrf']
    # print(csrftoken)
data = dict(test='hello from my darkness old friend', csrfmiddlewaretoken=csrftoken, next='/')
r = client.post(URL ,data=data)