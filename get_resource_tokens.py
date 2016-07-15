from requests_oauthlib import OAuth1Session
import config

try:
    input = raw_input
except NameError:
    pass


def get_resource_auth(client_key, client_secret):
    callback_uri = 'http://localhost/'

    oauth = OAuth1Session(client_key,
                          client_secret=client_secret,
                          callback_uri=callback_uri)

    request_token_uri = 'https://auth.aweber.com/1.0/oauth/request_token'
    fetch_response = oauth.fetch_request_token(request_token_uri)

    resource_owner_key = fetch_response.get('oauth_token')
    resource_owner_secret = fetch_response.get('oauth_token_secret')

    base_auth_url = 'https://auth.aweber.com/1.0/oauth/authorize?'
    auth_url = oauth.authorization_url(base_auth_url)

    print('Authorize here: {}'.format(auth_url))
    redirect_response = input('Enter the redirect URL: ')

    oauth_response = oauth.parse_authorization_response(redirect_response)
    verifier = oauth_response.get('oauth_verifier')

    access_token_url = 'https://auth.aweber.com/1.0/oauth/access_token'

    aweber_access = OAuth1Session(client_key,
                                  client_secret=client_secret,
                                  resource_owner_key=resource_owner_key,
                                  resource_owner_secret=resource_owner_secret,
                                  verifier=verifier)
    aweber_access_tokens = aweber_access.fetch_access_token(access_token_url)

    resource_owner_key = aweber_access_tokens['oauth_token']
    resource_owner_secret = aweber_access_tokens['oauth_token_secret']

    return (resource_owner_key, resource_owner_secret)


def get_resource_tokens():
    key, secret = get_resource_auth(config.CLIENT_KEY, config.CLIENT_SECRET)

    print("RESOURCE_OWNER_KEY = '{0}'".format(key))
    print("RESOURCE_OWNER_SECRET = '{0}'".format(secret))


if __name__ == '__main__':
    get_resource_tokens()
