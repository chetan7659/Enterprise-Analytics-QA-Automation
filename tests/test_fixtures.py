import pytest


@pytest.fixture(
    params=["admin", "analyst", "viewer"]
)
def user_role(request):
    return request.param


def test_user_role(user_role):
    print(user_role)

    assert user_role in [
        "admin",
        "analyst",
        "viewer",
    ]