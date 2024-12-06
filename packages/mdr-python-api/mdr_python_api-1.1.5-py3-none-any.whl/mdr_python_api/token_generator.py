from .input import start_input_thread
from jwcrypto import jwt
from .loop_back_server import LoopbackServer
from .oidc_common import OpenIDConfiguration, ClientConfiguration, get_client_state
import json
import logging
import os
import requests
import sys
import webbrowser
import time

cwd = os.getcwd()
current_file_path = os.path.dirname(os.path.abspath(__file__))

DEFAULT_PROVIDER = "https://czi-prod.okta.com"
DEFAULT_CLIENT_CONFIGURATION = f"{current_file_path}/code-flow.json"

client_configuration = DEFAULT_CLIENT_CONFIGURATION
openid_configuration = f"{DEFAULT_PROVIDER}/.well-known/openid-configuration"

# logging

# logging.basicConfig(level=logging.DEBUG)

provider = OpenIDConfiguration(openid_configuration)
client = ClientConfiguration(client_configuration)


def create_token() -> str:
    with LoopbackServer(provider, client) as httpd:
        # launch web browser
        webbrowser.open(httpd.base_uri)
        # wait for input
        start_input_thread("Press enter to stop\r\n", httpd.done)
        # process http requests until authorization response is received
        time.sleep(1)
        if httpd.wait_authorization_response() is None:
            sys.exit()

    # handles error from authorization response

    if "error" in httpd.authorization_response:
        raise Exception(httpd.authorization_response["error"][0])

    # verify state

    state = get_client_state(httpd.authorization_response)

    # token request with authorization code

    body = {
        "grant_type": "authorization_code",
        "redirect_uri": httpd.redirect_uri,
        "code": httpd.authorization_response["code"][0],
        "code_verifier": state.code_verifier,
    }
    # client authentication
    if client.client_secret is None:
        body["client_id"] = client.client_id
        auth = None
    else:
        auth = (client.client_id, client.client_secret)
        logging.debug(f"token_request_auth = {auth}")

    logging.debug(f"token_request_params = {body}")
    logging.debug(f"token_request = {provider.token_endpoint}")
    r = requests.post(provider.token_endpoint, data=body, auth=auth)
    token_response = r.json()
    logging.debug(f"token_response = {token_response}")

    # handles error from token response

    if "error" in token_response:
        raise Exception(token_response["error"])

    # invoke userinfo endpoint with access token

    if provider.userinfo_endpoint is not None and "access_token" in token_response:
        headers = {
            "Accept": "application/json",
            "Authorization": "Bearer " + token_response["access_token"],
        }
        r = requests.get(provider.userinfo_endpoint, headers=headers)
        r.raise_for_status()
        logging.info(json.dumps(r.json(), indent=2))

    # id_token

    if provider.provider_jwks is not None and "id_token" in token_response:
        # id_token - signature
        token = jwt.JWT(key=provider.provider_jwks, jwt=token_response["id_token"])
        id_token = json.loads(token.claims)
        # verify nonce
        if state.nonce != id_token["nonce"]:
            raise Exception("invalid nonce")
        logging.info(json.dumps(id_token, indent=2))
        return token_response["id_token"]
    return ""
