import os
import requests


def fetch_token(username, password):
    url = os.environ.get("KEYCLOAK_URL", "https://keycloak.manager.ingkle.dev")
    realm = os.environ.get("KEYCLOAK_REALM", "k8s")
    client_id = os.environ.get("KEYCLOAK_CLIENT_ID", "dot")
    client_secret = os.environ.get(
        "KEYCLOAK_CLIENT_SECRET", "fNTob9OCw9BSJ4qppkD6bz4KNqTXIFEW"
    )

    res = requests.post(
        "{}/auth/realms/{}/protocol/openid-connect/token".format(url, realm),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "username": username,
            "password": password,
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "password",
        },
    )
    if res.status_code == 200:
        return res.json()["access_token"]
    return None


def fetch_userinfo(token):
    url = os.environ.get("KEYCLOAK_URL", "https://keycloak.manager.ingkle.dev")
    realm = os.environ.get("KEYCLOAK_REALM", "k8s")

    res = requests.get(
        "{}/auth/realms/{}/protocol/openid-connect/userinfo".format(url, realm),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer {}".format(token),
        },
    )
    if res.status_code == 200:
        return res.json()
    return None
