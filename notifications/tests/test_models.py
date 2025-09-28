import pytest

from ..models import Notification


@pytest.fixture
def notification():
    return Notification.objects.create(
        users=[
            [
                "Тамир",
                "tamirmandreev@mail.ru",
                "89915410704",
            ],
            [
                "Тимур",
                "mandreevts@gmail.com",
                "+79644111469",
            ],
        ],
        subject="Тестовое письмо",
        message="Проводится тестирование создания объекта модели Notification",
    )


@pytest.mark.django_db
def test_notification_creation(notification):
    """
    Тестирует создание объекта модели Notification
    """
    assert notification.users == [
        [
            "Тамир",
            "tamirmandreev@mail.ru",
            "89915410704",
        ],
        [
            "Тимур",
            "mandreevts@gmail.com",
            "+79644111469",
        ],
    ]
    assert notification.subject == "Тестовое письмо"
    assert (
        notification.message
        == "Проводится тестирование создания объекта модели Notification"
    )
