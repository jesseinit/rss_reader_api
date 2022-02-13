import pytest
from pytest_factoryboy import register

from feedservice.tests.factories import FeedFactory
from userservice.tests.factories import UserFactory

register(UserFactory, "user_one", username="jesseinit", email="john.doe@mail.com")
register(UserFactory, "user_two", username="user_two", email="user_two@mail.com")


class DotDict:
    # Help Gotten from https://stackoverflow.com/questions/1305532/convert-nested-python-dict-to-object
    def __init__(self, d: dict):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [DotDict(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, DotDict(b) if isinstance(b, dict) else b)


@pytest.fixture(autouse=True)
def whitenoise_autorefresh(settings):
    """
    Get rid of whitenoise "No directory at" warning, as it's not helpful when running tests.

    Related:
        - https://github.com/evansd/whitenoise/issues/215
        - https://github.com/evansd/whitenoise/issues/191
        - https://github.com/evansd/whitenoise/commit/4204494d44213f7a51229de8bc224cf6d84c01eb
    """
    settings.WHITENOISE_AUTOREFRESH = True


@pytest.fixture()
def user_one_token(user_one, client):
    response = client.post(
        "/api/v1/auth/login",
        {"username": user_one.username, "password": "K1#EzbuXsFWZ"},
    )
    return {
        "content_type": "application/json",
        "HTTP_AUTHORIZATION": f"Bearer {response.json()['data']['token']['access']}",
    }


@pytest.fixture()
def user_two_token(user_two, client):
    response = client.post(
        "/api/v1/auth/login",
        {"username": user_two.username, "password": "K1#EzbuXsFWZ"},
    )
    return {
        "content_type": "application/json",
        "HTTP_AUTHORIZATION": f"Bearer {response.json()['data']['token']['access']}",
    }


@pytest.fixture()
def feed_response():
    data = {
        "entries": [
            {
                "title": "Grote toestroom tijdens actie De Nacht staat op, eerste clubs gesloten",
                "link": "https://www.nu.nl/coronavirus/6183778/grote-toestroom-tijdens-actie-de-nacht-staat-op-eerste-clubs-gesloten.html",
                "summary": "Tegen de coronamaatregelen in hebben nachtclubs zaterdagavond de deuren geopend in het kader van de actie 'De Nacht staat op'.",
                "published": "Sun, 13 Feb 2022 02:50:35 +0100",
                "id": "https://www.nu.nl/-/6183778/",
            },
            {
                "title": "Grote toestroom tijdens actie De Nacht staat op, eerste clubs gesloten",
                "link": "https://www.nu.nl/coronavirus/6183778/grote-toestroom-tijdens-actie-de-nacht-staat-op-eerste-clubs-gesloten.html",
                "summary": "Tegen de coronamaatregelen in hebben nachtclubs zaterdagavond de deuren geopend in het kader van de actie 'De Nacht staat op'.",
                "published": "Sun, 13 Feb 2022 02:50:35 +0100",
                "id": "https://www.nu.nl/-/6183778/",
            },
            {
                "title": "Zes gewonden door ongeluk in De Mortel, bestuurder van auto is aangehouden",
                "link": "https://www.nu.nl/algemeen/6183790/zes-gewonden-door-ongeluk-in-de-mortel-bestuurder-van-auto-is-aangehouden.html",
                "summary": "Door een eenzijdig ongeval in De Mortel (Noord-Brabant) zijn zaterdagavond laat zes inzittenden van een auto gewond geraakt",
                "published": "Sun, 13 Feb 2022 02:50:35 +0100",
                "id": "https://www.nu.nl/-/6183790/",
            },
        ],
        "feed": {
            "title": "NU - Ander nieuws",
            "updated": "Sun, 13 Feb 2022 02:50:35 +0100",
        },
    }

    return DotDict(data)
