import pytest

from notifications.models import User
from notifications.services import create_users


@pytest.mark.django_db
def test_create_users():
    data = [
        ['Тамир', 'tamirmandreev@mail.ru', '89915410704'],
        ['Тимур', 'mandreevts@gmail.com', '+79644111469'],
    ]

    assert User.objects.all().count() == 0
    create_users(data)
    assert User.objects.all().count() == len(data)

    tamir_user = User.objects.get(email='tamirmandreev@mail.ru')
    timur_user = User.objects.get(email='mandreevts@gmail.com')

    assert tamir_user.name == 'Тамир'
    assert tamir_user.email == 'tamirmandreev@mail.ru'
    assert tamir_user.number == '89915410704'

    assert timur_user.name == 'Тимур'
    assert timur_user.email == 'mandreevts@gmail.com'
    assert timur_user.number == '+79644111469'
