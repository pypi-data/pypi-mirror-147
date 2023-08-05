import os
import requests


def fetch_token(
    username,
    password,
    url=os.environ.get("KEYCLOAK_URL", ""),
    realm=os.environ.get("KEYCLOAK_REALM", ""),
    client_id=os.environ.get("KEYCLOAK_CLIENT_ID", ""),
    client_secret=os.environ.get("KEYCLOAK_CLIENT_SECRET", ""),
):
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


def fetch_userinfo(
    token,
    url=os.environ.get("KEYCLOAK_URL", ""),
    realm=os.environ.get("KEYCLOAK_REALM", ""),
):
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
