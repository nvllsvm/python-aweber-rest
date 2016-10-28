#!/usr/bin/env python3
import argparse
from urllib.parse import parse_qs
from urllib.parse import urlencode
from urllib.parse import urljoin
from urllib.parse import urlparse

from requests_oauthlib import OAuth1Session


def get_auth_url(app_id, callback_url):
    base_auth_url = 'https://auth.aweber.com/1.0/oauth/authorize_app/'
    url = urljoin(base_auth_url, app_id)
    qs = urlencode({'oauth_callback': callback_url})
    return '{}?{}'.format(url, qs)


def parse_authorization_url(url):
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    authorization = qs['authorization_code'][0].split('|')

    credentials = {}
    credentials['client_key'] = authorization[0]
    credentials['client_secret'] = authorization[1]
    credentials['resource_owner_key'] = authorization[2]
    credentials['resource_owner_secret'] = authorization[3]
    credentials['verifier'] = authorization[4]

    return credentials


def get_access_tokens(url):
    credentials = parse_authorization_url(url)

    session = OAuth1Session(**credentials)

    access_url = 'https://auth.aweber.com/1.0/oauth/access_token'
    response = session.fetch_access_token(access_url)

    access_token = response['oauth_token']
    access_secret = response['oauth_token_secret']

    return access_token, access_secret


def main():
    parser = argparse.ArgumentParser(
            description='AWeber API authorization utility.')
    parser.add_argument('-a', '--appid')
    parser.add_argument('-c', '--callback')
    parser.add_argument('-r', '--redirect')
    args = parser.parse_args()

    if args.appid or args.callback:
        if not args.appid or not args.callback:
            print('Both appid and callback must be specified.')
            parser.print_help()
            exit()
        auth_url = get_auth_url(args.appid, args.callback)
        print('Auth URL: ', auth_url)
    elif args.redirect:
        access_token, access_secret = get_access_tokens(args.redirect)
        print('access_token: ', access_token)
        print('access_secret: ', access_secret)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
