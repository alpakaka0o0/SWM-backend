# This file is for Pytest Configuration
# This file is used to define fixtures that can be used in multiple test files

import random
from unittest.mock import Mock

import pytest
from faker import Faker
from rest_framework.test import APIClient

from todos.models import Category, SubTodo, Todo, User

client = APIClient()

fake = Faker()


@pytest.fixture(scope="module")
def invalid_token():
    response = {
        "token": "token",
        "deviceToken": "device_token",
        "type": 0,
    }
    return response


@pytest.fixture
def create_user(db):
    user = User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="testpassword",
    )
    return user


@pytest.fixture
def authenticated_client(create_user):
    client.force_authenticate(user=create_user, token={"device": None})
    yield client
    client.force_authenticate(user=None)  # logout


@pytest.fixture
def create_category(
    db,
    create_user,
    title="Test Category",
    color=1,
    rank="0|hzzzzz:",
):
    category = Category.objects.create(
        user_id=create_user,
        title=title,
        color=color,
        rank=rank,
    )
    return category


@pytest.fixture
def create_todo(
    db,
    create_user,
    create_category,
    date="2024-08-01",
    due_time=None,
    content="Test Todo",
    is_completed=False,
    rank="0|hzzzzz:",
):
    todo = Todo.objects.create(
        user_id=create_user,
        date=date,
        due_time=due_time,
        category_id=create_category,
        content=content,
        is_completed=is_completed,
        rank=rank,
    )
    return todo


@pytest.fixture
def create_subtodo(
    db,
    create_todo,
    content="Test SubTodo",
    date="2024-08-01",
    due_time=None,
    is_completed=False,
    rank="0|hzzzzz:",
):
    subtodo = SubTodo.objects.create(
        content=content,
        date=date,
        due_time=due_time,
        todo=create_todo,
        is_completed=is_completed,
        rank=rank,
    )
    return subtodo


@pytest.fixture
def date():
    return fake.date_this_year()


@pytest.fixture
def content():
    return fake.sentence(nb_words=6)


@pytest.fixture
def rank():
    orders = ["0|hzzzzz:", "0|i00007:", "0|i0000f:"]
    return orders


@pytest.fixture
def color():
    return fake.random_int(min=0, max=8)


@pytest.fixture
def title():
    return fake.sentence(nb_words=3)


@pytest.fixture
def category():
    CATEGORY_CHOICES = [
        ("bug", "버그"),
        ("feature", "기능 요청"),
        ("feedback", "일반 피드백"),
    ]
    return random.choice(CATEGORY_CHOICES)[0]


@pytest.fixture
def due_time():
    return fake.time(pattern="%H:%M:%S")


@pytest.fixture
def recommend_result():
    mock_response = Mock()
    mock_response.choices = [
        Mock(
            message=Mock(
                content=(
                    '{"id": 1, "content": "study algebra", "date": "2024-09-01", '  # noqa: E501
                    '"due_time": "None", "category_id": 1, '
                    '"is_completed": false, "children": []}'
                )
            )
        )
    ]

    return mock_response


# FCM 알림 함수를 기본적으로 disable하는 fixture
@pytest.fixture(autouse=True)
def patch_send_push_notification_device(monkeypatch):
    monkeypatch.setattr(
        "todos.firebase_messaging.send_push_notification_device",
        lambda *args, **kwargs: None,
    )
