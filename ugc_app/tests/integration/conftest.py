from typing import Iterator
from http import HTTPStatus

import httpx
import pytest
from fastapi.testclient import TestClient

from app import app  # type: ignore[import-not-found]


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(app) as client:
        yield client


def assert_created(response: httpx.Response) -> None:
    assert response.status_code == HTTPStatus.CREATED


def assert_deleted(response: httpx.Response) -> None:
    assert response.status_code == HTTPStatus.NO_CONTENT
