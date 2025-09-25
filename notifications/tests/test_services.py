import pytest

from notifications.models import User
from notifications.services import create_users
from notifications.models import User
from notifications.services import send_email_message



from django.core import mail

@pytest.mark.django_db
def test_create_users():
    data = [
        ['Тамир', 'tamirmandreev@mail.ru', '89915410704', '747451276'],
        ['Тимур', 'mandreevts@gmail.com', '+79644111469', '747451276'],
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


class TestSendEmailMessage:
    '''
    Тестирует функцию send_email_message
    '''

    @pytest.fixture
    def users(self):
        user_1 = User.objects.create(name='Tamir', email='tamirmandreev@mail.ru', number='+79915410704', tg_chat_id='747451276')
        user_2 = User.objects.create(name='Timur', email='mandreevts@gmail.com', number='+79644111469', tg_chat_id='747451276')

    @pytest.mark.django_db
    def test_send_async_email_success(self, users):
        '''
        Тестирует успешность отправки сообщения
        :return:
        '''
        send_email_message('Test subject', 'Test message')
        assert len(mail.outbox) == 2
        assert mail.outbox[0].subject == 'Test subject'
        assert mail.outbox[0].to == ['tamirmandreev@mail.ru']
        assert mail.outbox[0].body == 'Test message'
        assert mail.outbox[0].from_email == 'tamirmandreev@mail.ru'
        assert mail.outbox[1].subject == 'Test subject'
        assert mail.outbox[1].to == ['mandreevts@gmail.com']
        assert mail.outbox[1].body == 'Test message'
        assert mail.outbox[1].from_email == 'tamirmandreev@mail.ru'

    def test_send_async_email_failure(self):
        '''
        Тестирует обработку ошибок
        :return:
        '''
        with pytest.raises(Exception):
            send_email_message('', '', [])
