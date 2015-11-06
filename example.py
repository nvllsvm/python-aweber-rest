import json
from aweber_rest import api

account_id = ''
list_id = ''

url = 'https://api.aweber.com/1.0/accounts/{0}/lists/{1}/subscribers'.format(account_id, list_id)
args = {}

response = api.call(url, args)

subscribers = response.json()['entries']

while 'next_collection_link' in response.json().keys():
    url = response.json()['next_collection_link']

    response = api.call(url, args)

    subscribers += response.json()['entries']

for s in subscribers:
    print(json.dumps(s, sort_keys=True, indent=4))
