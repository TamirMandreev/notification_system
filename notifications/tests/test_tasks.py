import pytest

from notifications.tasks import send_async_email

from django.core import mail

from notifications.models import User


class TestSendAsyncEmail:
    '''
    Тестирует функцию send_async_email
    '''

    @pytest.fixture
    def users(self):
        user_1 = User.objects.create(name='Tamir', email='tamirmandreev@mail.ru', number='89915410704')
        user_2 = User.objects.create(name='Timur', email='mandreevts@gmail.com', number='+79644111469')

    @pytest.mark.django_db
    def test_send_async_email_success(self, users):
        '''
        Тестирует успешность отправки сообщения
        :return:
        '''
        send_async_email('Test subject', 'Test message')
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
            send_async_email('', '', [])
