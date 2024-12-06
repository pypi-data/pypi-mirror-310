from typing import Tuple
import requests
from .token_manager import TokenManager

HOST = "https://chief-woodcock.dev-ml-platform.dev.czi.team"  # Standard loopback interface address (localhost)
PORT = 443  # Port to listen on (non-privileged ports are > 1023)
OIDC = True


def encode(string: str):
    return string.replace("/", chr(0xFF))


token_manager = TokenManager()


class ApiImpl:
    def local_machine():
        global OIDC
        OIDC = False

    def generate_auth_headers(new_token=False):
        if not OIDC:
            return {}
        auth_token = token_manager.get_token(new_token)
        headers = {"Authorization": f"Bearer {auth_token}"}
        return headers

    def init(new_host, new_port=443):
        global HOST
        global PORT
        HOST = new_host
        PORT = new_port

    def send_request_internal(method, url, params, headers, json=False):
        if params is None and not json:
            return requests.request(method=method, url=url, headers=headers)
        if json:
            return requests.request(
                method=method, url=url, json=params, headers=headers
            )
        return requests.request(method=method, url=url, params=params, headers=headers)

    def send_request(method, url, params, json=False):
        headers = ApiImpl.generate_auth_headers()
        response = ApiImpl.send_request_internal(
            method=method, url=url, params=params, headers=headers, json=json
        )
        if response.raise_for_status() is not None:
            headers = ApiImpl.generate_auth_headers(True)
            response = ApiImpl.send_request_internal(
                method=method, url=url, params=params, headers=headers, json=json
            )
            return response
        return response

    def add_dependencies(
        id: str,
        org: str,
        domain: str,
        label: str,
        version: str,
        dependencies: list[Tuple[str, str, str, str, str]],
        input_dep: bool,
    ):
        for dep in dependencies:
            dep_id, dep_org, dep_domain, dep_label, dep_version, tag = dep
            input_dep_str = "false"
            if input_dep:
                input_dep_str = "true"

            url = f"{HOST}:{PORT}/dependency"
            params = {
                "id": id,
                "org": org,
                "domain": domain,
                "label": label,
                "version": version,
                "dep_id": dep_id,
                "dep_org": dep_org,
                "dep_domain": dep_domain,
                "dep_label": dep_label,
                "dep_version": dep_version,
                "tag": tag,
                "input_dep": input_dep_str,
            }
            ApiImpl.send_request(method="post", url=url, params=params)

    def register_meta_data(
        id: str,
        org: str,
        domain: str,
        label: str,
        version: str,
        owner: str,
        reg_url: str,
        md: str,
    ) -> str:
        url = f"{HOST}:{PORT}/register"
        params = {
            "id": id,
            "org": org,
            "domain": domain,
            "label": label,
            "version": version,
            "owner": owner,
            "url": reg_url,
            "md": md,
        }

        response = ApiImpl.send_request(
            method="post", url=url, params=params, json=True
        )
        return response.text

    def search_label(search_string: str):
        url = f"{HOST}:{PORT}/search"
        params = {
            "regex": search_string,
            "regex_search": "false",
            "dependencies": "false",
        }
        response = ApiImpl.send_request(method="get", url=url, params=params)
        delimiter = chr(0xFF)
        results = response.text.split(delimiter)
        return results

    def search(search_string: str):
        url = f"{HOST}:{PORT}/search"
        params = {
            "regex": search_string,
            "regex_search": "true",
            "dependencies": "false",
        }
        response = ApiImpl.send_request(method="get", url=url, params=params)
        delimiter = chr(0xFF)
        results = response.text.split(delimiter)
        return results

    def search_dependencies(search_string: str):
        url = f"{HOST}:{PORT}/search"
        params = {
            "regex": search_string,
            "regex_search": "true",
            "dependencies": "true",
        }
        response = ApiImpl.send_request(method="get", url=url, params=params)
        delimiter = chr(0xFF)
        results = response.text.split(delimiter)
        return results

    def health_check():
        url = f"{HOST}:{PORT}/health"
        print(f"URL = {url}")
        try:
            response = ApiImpl.send_request(method="get", url=url, params=None)
            result = response.text
        except Exception:
            return False
        if result == "OK":
            return True
        return False

    def kv_insert(key: str, value: str, id: str, org: str, domain: str, version: str):
        url = f"{HOST}:{PORT}/kv_insert"
        params = {
            "key": key,
            "value": value,
            "id": id,
            "org": org,
            "domain": domain,
            "version": version,
        }
        response = ApiImpl.send_request(method="post", url=url, params=params)
        return response.text

    def kv_search(regex: str) -> str:
        url = f"{HOST}:{PORT}/kv_search"
        params = {
            "regex": regex,
        }
        response = ApiImpl.send_request(method="get", url=url, params=params)
        return response.text

    def kv_put(key: str, value: str):
        url = f"{HOST}:{PORT}/kv_put"
        params = {
            "key": key,
            "value": value,
        }
        response = ApiImpl.send_request(method="post", url=url, params=params)
        return response.text

    def kv_get(key: str):
        url = f"{HOST}:{PORT}/kv_get"
        params = {
            "key": key,
        }
        response = ApiImpl.send_request(method="get", url=url, params=params)
        return response.text

    def kv_delete(key: str):
        url = f"{HOST}:{PORT}/kv_delete"
        params = {
            "key": key,
        }
        response = ApiImpl.send_request(method="post", url=url, params=params)
        return response.text
