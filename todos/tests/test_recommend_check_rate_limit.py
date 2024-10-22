# import asyncio
import time
from unittest.mock import AsyncMock, patch

import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
@pytest.mark.asyncio
@patch(
    "todos.views.openai_client.chat.completions.create", new_callable=AsyncMock
)
def test_rate_limit_exceeded(
    mock_llm, authenticated_client, create_todo, recommend_result
):
    mock_llm.return_value = recommend_result
    url = reverse("recommend")

    response = authenticated_client.get(url, {"todo_id": create_todo.id})
    assert response.status_code == status.HTTP_200_OK

    response = authenticated_client.get(url, {"todo_id": create_todo.id})
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert response.json()["error"] == "Rate limit exceeded"


@pytest.mark.django_db
@patch(
    "todos.views.openai_client.chat.completions.create", new_callable=AsyncMock
)
def test_rate_limit_passed(
    mock_llm, authenticated_client, create_todo, recommend_result
):
    url = reverse("recommend")
    mock_llm.return_value = recommend_result

    response = authenticated_client.get(url, {"todo_id": create_todo.id})
    assert response.status_code == status.HTTP_200_OK

    time.sleep(10)

    response = authenticated_client.get(url, {"todo_id": create_todo.id})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
@patch(
    "todos.views.openai_client.chat.completions.create", new_callable=AsyncMock
)
def test_rate_limit_premium(
    mock_llm, authenticated_client, create_user, create_todo, recommend_result
):
    create_user.is_premium = True
    create_user.save()

    url = reverse("recommend")
    mock_llm.return_value = recommend_result

    response = authenticated_client.get(url, {"todo_id": create_todo.id})
    assert response.status_code == status.HTTP_200_OK

    response = authenticated_client.get(url, {"todo_id": create_todo.id})
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_time_openAI(authenticated_client, create_todo, benchmark):
    url = reverse("recommend")

    response = benchmark(
        lambda: authenticated_client.get(url, {"todo_id": create_todo.id})
    )
    assert response.status_code == status.HTTP_200_OK
