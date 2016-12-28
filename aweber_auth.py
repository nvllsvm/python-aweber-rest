import argparse

try:
    from urllib.parse import parse_qs
    from urllib.parse import urlencode
    from urllib.parse import urljoin
    from urllib.parse import urlparse
except ImportError:
    from urllib import urlencode
    from urlparse import parse_qs
    from urlparse import urljoin
    from urlparse import urlparse

from requests_oauthlib import OAuth1Session
from requests_oauthlib.oauth1_session import TokenRequestDenied


def get_auth_url(app_id, callback_url):
    base_auth_url = 'https://auth.aweber.com/1.0/oauth/authorize_app/'
    url = urljoin(base_auth_url, app_id)
    qs = urlencode({'oauth_callback': callback_url})
    return '{}?{}'.format(url, qs)


def parse_authorization_url(url):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    authorization = qs['authorization_code'][0].split('|')

    tokens = {}
    tokens['client_key'] = authorization[0]
    tokens['client_secret'] = authorization[1]
    tokens['resource_owner_key'] = authorization[2]
    tokens['resource_owner_secret'] = authorization[3]
    tokens['verifier'] = authorization[4]

    return tokens


def get_access_tokens(redirect_url):
    request_tokens = parse_authorization_url(redirect_url)
    session = OAuth1Session(**request_tokens)

    access_url = 'https://auth.aweber.com/1.0/oauth/access_token'
    try:
        response = session.fetch_access_token(access_url)
    except TokenRequestDenied as e:
        print(e)
        exit(1)

    values = {}
    values['client_key'] = request_tokens['client_key']
    values['client_secret'] = request_tokens['client_secret']
    values['resource_owner_key'] = response['oauth_token']
    values['resource_owner_secret'] = response['oauth_token_secret']

    return values


def main():
    parser = argparse.ArgumentParser(
            description='AWeber API authorization utility.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-r', dest='request', nargs=2,
                       metavar=('APP_ID', 'CALLBACK_URL'),
                       help='retrieve request tokens')
    group.add_argument('-a', dest='access',
                       metavar='REDIRECT_URL',
                       help='retrieve access tokens')
    args = parser.parse_args()

    if args.request:
        auth_url = get_auth_url(args.request[0], args.request[1])
        print(auth_url)
    elif args.access:
        tokens = get_access_tokens(args.access)

        def print_row(key):
            print('{} = {}'.format(key, tokens[key]))

        print_row('client_key')
        print_row('client_secret')
        print_row('resource_owner_key')
        print_row('resource_owner_secret')
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
