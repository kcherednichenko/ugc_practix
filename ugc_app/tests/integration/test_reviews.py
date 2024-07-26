from http import HTTPStatus
from typing import List, Dict
from uuid import uuid4

from fastapi.testclient import TestClient
import httpx

from conftest import assert_created, assert_deleted
from utils import get_random_user


def test_add_review_forbidden_no_auth(client: TestClient) -> None:
    filmwork_id = uuid4()
    response = client.post(f"api/v1/filmworks/{filmwork_id}/reviews", json={'title': 'title', 'text': 'text'})
    assert response.status_code == HTTPStatus.FORBIDDEN


def test_get_reviews_correctly(client: TestClient) -> None:
    user1, user2 = get_random_user(), get_random_user()
    filmwork_id = uuid4()
    review_to_post1, review_to_post2 = {'title': 'title 1', 'text': 'text 1'}, {'title': 'title 2', 'text': 'text 2'}
    review_to_assert1 = {'title': 'title 1', 'text': 'text 1', 'filmwork_id': str(filmwork_id), 'id': str(user1.id),
                         'likes': [str(user1.id)]}
    review_to_assert2 = {'title': 'title 2', 'text': 'text 2', 'filmwork_id': str(filmwork_id), 'id': str(user2.id),
                         'likes': [str(user2.id)]}

    assert_created(
        client.post(
            f"api/v1/filmworks/{filmwork_id}/reviews",
            json=review_to_post1,
            headers={"Authorization": f"Bearer {user1.token}"},
        )
    )
    assert_created(
        client.post(
            f"api/v1/filmworks/{filmwork_id}/reviews",
            json=review_to_post2,
            headers={"Authorization": f"Bearer {user2.token}"},
        )
    )

    assert_created(
        client.post(
            f"api/v1/filmworks/{filmwork_id}/reviews/{user1.id}/likes",
            headers={"Authorization": f"Bearer {user1.token}"}
        )
    )
    assert_created(
        client.post(
            f"api/v1/filmworks/{filmwork_id}/reviews/{user2.id}/likes",
            headers={"Authorization": f"Bearer {user2.token}"}
        )
    )

    _assert_reviews(
        client.get(f"api/v1/filmworks/{filmwork_id}/reviews", headers={"Authorization": f"Bearer {user1.token}"}),
        [review_to_assert1, review_to_assert2],
    )

    assert_deleted(
        client.delete(
            f"api/v1/filmworks/{filmwork_id}/reviews",
            headers={"Authorization": f"Bearer {user1.token}"},
        )
    )
    assert_deleted(
        client.delete(
            f"api/v1/filmworks/{filmwork_id}/reviews",
            headers={"Authorization": f"Bearer {user2.token}"},
        )
    )

    _assert_reviews(
        client.get(f"api/v1/filmworks/{filmwork_id}/reviews", headers={"Authorization": f"Bearer {user1.token}"}),
        [],
    )


def _assert_reviews(response: httpx.Response, expected_reviews: List[Dict]) -> None:
    assert response.status_code == HTTPStatus.OK
    actual_reviews = response.json()
    parsed_actual_reviews = []
    for review in actual_reviews:
        review.pop("created_at", None)
        parsed_actual_reviews.append(review)
    assert parsed_actual_reviews == expected_reviews
