import pytest

from notifications.tasks import send_async_email

from django.core import mail


class TestSendAsyncEmail:
    '''
    Тестирует функцию send_async_email
    '''

    def test_send_async_email_success(self):
        '''
        Тестирует успешность отправки сообщения
        :return:
        '''
        send_async_email('Test subject', 'Test message')
        assert len(mail.outbox) == 1
        assert mail.outbox[0].subject == 'Test subject'
        assert mail.outbox[0].to == ['tamirmandreev@mail.ru', 'mandreevts@gmail.com']
        assert mail.outbox[0].body == 'Test message'
        assert mail.outbox[0].from_email == 'tamirmandreev@mail.ru'

    def test_send_async_email_failure(self):
        '''
        Тестирует обработку ошибок
        :return:
        '''
        with pytest.raises(Exception):
            send_async_email('', '', [])
