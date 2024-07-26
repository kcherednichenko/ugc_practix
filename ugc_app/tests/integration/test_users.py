from uuid import uuid4
from http import HTTPStatus

from fastapi.testclient import TestClient
import httpx

from conftest import assert_created, assert_deleted
from utils import get_random_user


def test_add_bookmark_forbidden_no_auth(client: TestClient) -> None:
    filmwork_id = uuid4()
    response = client.post("api/v1/users/bookmarks", json={"filmwork_id": str(filmwork_id)})
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_get_bookmarks_correctly(client: TestClient) -> None:
    user = get_random_user()
    filmwork_id_one, filmwork_id_two = uuid4(), uuid4()
    assert_created(
        client.post(
            "api/v1/users/bookmarks",
            json={"filmwork_id": str(filmwork_id_one)},
            headers={"Authorization": f"Bearer {user.token}"},
        )
    )
    assert_created(
        client.post(
            "api/v1/users/bookmarks",
            json={"filmwork_id": str(filmwork_id_two)},
            headers={"Authorization": f"Bearer {user.token}"},
        )
    )
    _assert_bookmarks(
        client.get("api/v1/users/bookmarks", headers={"Authorization": f"Bearer {user.token}"}),
        [str(filmwork_id_one), str(filmwork_id_two)],
    )

    assert_deleted(
        client.delete(
            f"api/v1/users/bookmarks/{filmwork_id_one}",
            headers={"Authorization": f"Bearer {user.token}"},
        )
    )
    assert_deleted(
        client.delete(
            f"api/v1/users/bookmarks/{filmwork_id_two}",
            headers={"Authorization": f"Bearer {user.token}"},
        )
    )
    _assert_bookmarks(
        client.get("api/v1/users/bookmarks", headers={"Authorization": f"Bearer {user.token}"}),
        [],
    )


def _assert_bookmarks(response: httpx.Response, expected_bookmarks: list[str]) -> None:
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"filmworks": expected_bookmarks}
