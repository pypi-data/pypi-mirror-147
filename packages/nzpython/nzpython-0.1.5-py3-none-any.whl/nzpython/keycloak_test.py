from .keycloak import fetch_userinfo


def test_keycloak():
    try:
        userinfo = fetch_userinfo(
            "",
            url="https://keycloak.manager.ingkle.dev",
            realm="k8s",
        )
        assert userinfo is None
    except:
        assert False
