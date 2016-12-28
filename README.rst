python-aweber-rest
==================
A Python example for interacting with the AWeber REST API using requests-oauthlib_.

``aweber_auth.py`` can be used either as a module or as a command-line utility.

Authentication
--------------
The first step involves the AWeber customer authenticating with the integration on a app-specific AWeber page. The URL will contain your integration's app ID and a URL in which users will be redirected to upon successful authentication.

**Python**

.. code-block:: python

    aweber_auth.get_auth_url(app_id, callback_url)

**Command-Line**

.. code-block:: bash

    python aweber_auth.py -r <app_id> <callback_url>

The redirect URL will include the OAuth parameters used in both requesting the access tokens and connecting to the API. Simply pass the full redirect URL, including query string, to retrieve all OAuth tokens necessary for API use.

**Python**

.. code-block:: python

    aweber_auth.get_access_tokens(redirect_url)

**Command-Line**

.. code-block:: bash

    python aweber_auth.py -r <redirect_url>

Requests
--------
Usage of tokens retrieved during Authentication_ is demonstrated in the included ``example.py``.

.. _requests-oauthlib: https://pypi.python.org/pypi/requests-oauthlib
