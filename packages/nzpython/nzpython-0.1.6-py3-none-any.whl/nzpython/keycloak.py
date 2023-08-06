import os
import requests


def fetch_token(
    username,
    password,
    url=None,
    realm=None,
    client_id=None,
    client_secret=None,
):
    if url is None:
        url = os.environ.get("KEYCLOAK_URL")
    if realm is None:
        realm = os.environ.get("KEYCLOAK_REALM")
    if client_id is None:
        client_id = os.environ.get("KEYCLOAK_CLIENT_ID")
    if client_secret is None:
        client_secret = os.environ.get("KEYCLOAK_CLIENT_SECRET")

    res = requests.post(
        "{}/auth/realms/{}/protocol/openid-connect/token".format(url, realm),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "password",
            "username": username,
            "password": password,
        },
    )
    if res.status_code < 200 or res.status_code >= 300:
        res.raise_for_status()
    return res.json()


def refresh_token(
    refresh_token,
    url=None,
    realm=None,
    client_id=None,
    client_secret=None,
):
    if url is None:
        url = os.environ.get("KEYCLOAK_URL")
    if realm is None:
        realm = os.environ.get("KEYCLOAK_REALM")
    if client_id is None:
        client_id = os.environ.get("KEYCLOAK_CLIENT_ID")
    if client_secret is None:
        client_secret = os.environ.get("KEYCLOAK_CLIENT_SECRET")

    res = requests.post(
        "{}/auth/realms/{}/protocol/openid-connect/token".format(url, realm),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
        },
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
    )
    if res.status_code < 200 or res.status_code >= 300:
        res.raise_for_status()
    return res.json()


def fetch_userinfo(
    access_token,
    url=None,
    realm=None,
):
    if url is None:
        url = os.environ.get("KEYCLOAK_URL")
    if realm is None:
        realm = os.environ.get("KEYCLOAK_REALM")

    res = requests.get(
        "{}/auth/realms/{}/protocol/openid-connect/userinfo".format(url, realm),
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Bearer {}".format(access_token),
        },
    )
    if res.status_code < 200 or res.status_code >= 300:
        res.raise_for_status()
    return res.json()
