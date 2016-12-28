import pprint

from requests_oauthlib import OAuth1Session

client_key = ''
client_secret = ''
resource_owner_key = ''
resource_owner_secret = ''

aweber = OAuth1Session(client_key, client_secret,
                       resource_owner_key, resource_owner_secret)

url = 'https://api.aweber.com/1.0/accounts'

response = aweber.get(url)

print('Response code:', response.status_code)
pprint.pprint(response.json())
