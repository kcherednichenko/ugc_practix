from uuid import uuid4
from http import HTTPStatus

from fastapi.testclient import TestClient

from conftest import assert_created, assert_deleted
from utils import get_random_user


def test_add_score_for_filmwork_forbidden_no_auth(client: TestClient) -> None:
    filmwork_id = uuid4()
    response = client.post(f"api/v1/filmworks/{filmwork_id}/score", json={"score": 5})
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_average_score_is_correct(client: TestClient) -> None:
    user_one, score_one = get_random_user(), 5
    user_two, score_two = get_random_user(), 7
    filmwork_id = uuid4()
    assert_created(
        client.post(
            f"api/v1/filmworks/{filmwork_id}/score",
            json={"score": score_one},
            headers={"Authorization": f"Bearer {user_one.token}"},
        )
    )
    assert_created(
        client.post(
            f"api/v1/filmworks/{filmwork_id}/score",
            json={"score": score_two},
            headers={"Authorization": f"Bearer {user_two.token}"},
        )
    )

    response = client.get(f"api/v1/filmworks/{filmwork_id}/average-score")
    assert response.json() == {"avg_score": (score_one + score_two) / 2}

    assert_deleted(
        client.delete(
            f"api/v1/filmworks/{filmwork_id}/score",
            headers={"Authorization": f"Bearer {user_one.token}"},
        )
    )
    assert_deleted(
        client.delete(
            f"api/v1/filmworks/{filmwork_id}/score",
            headers={"Authorization": f"Bearer {user_two.token}"},
        )
    )

    response = client.get(f"api/v1/filmworks/{filmwork_id}/average-score")
    assert response.status_code == HTTPStatus.NOT_FOUND
