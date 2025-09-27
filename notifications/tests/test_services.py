import unittest

import pytest

from unittest.mock import patch, MagicMock
from django.conf import settings

from notifications.services import create_users
from notifications.models import User, EmailSendStatus, TelegramSendStatus
from notifications.services import send_email_message, send_telegram_message, send_sms_message

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


@pytest.fixture
def users():
    user1 = User.objects.create(name='Tamir', email='tamirmandreev@mail.ru', number='+79915410704',
                                tg_chat_id='747451276')
    user2 = User.objects.create(name='Timur', email='mandreevts@gmail.com', number='+79644111469',
                                tg_chat_id='747451276')
    return user1, user2


class TestSendEmailMessage:
    '''
    Тестирует функцию send_email_message
    '''

    @pytest.mark.django_db
    def test_send_email_message(self, users):
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

    def test_send_email_message_failure(self):
        '''
        Тестирует обработку ошибок
        :return:
        '''
        with pytest.raises(Exception):
            send_email_message('', '', [])


@pytest.mark.usefixtures('failed_email_statuses')
class TestSendTelegramMessage:

    @pytest.fixture
    def failed_email_statuses(self, users):
        '''
        Создает объекты, хранящие информацию о пользователях, которым не удалось отправить email-сообщение
        '''

        failed_email_statuse1 = EmailSendStatus.objects.create(user=users[0], is_successful=False)
        failed_email_statuses2 = EmailSendStatus.objects.create(user=users[1], is_successful=False)

    @pytest.fixture
    def mock_requests(self):
        with patch('notifications.services.requests.get') as mock_request_get:
            yield mock_request_get

    @pytest.mark.django_db
    def test_successful_telegram_send(self, mock_requests, failed_email_statuses):
        '''
        Тест успешной отправки уведомления в Telegram
        :param mock_requests:
        :param emails_send_status_false:
        :return:
        '''

        # Мок успешного ответа от Telegram API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_requests.return_value = mock_response

        send_telegram_message('Test subject', 'Test message')

        expected_calls = [
            unittest.mock.call(
                f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage',
                params={
                    'text': 'Тема: Test subject \n\nСообщение: Test message',
                    'chat_id': '747451276'
                }
            ),
            unittest.mock.call(f'{settings.TELEGRAM_URL}{settings.TELEGRAM_TOKEN}/sendMessage',
                               params={
                                   'text': 'Тема: Test subject \n\nСообщение: Test message',
                                   'chat_id': '747451276'
                               })
        ]
        mock_requests.assert_has_calls(expected_calls, any_order=True)


class TestSendSmsMessage:

    @pytest.fixture
    def mock_sms_aero(self):
        with patch('notifications.services.SmsAero') as mock_sms:
            yield mock_sms

    @pytest.fixture
    def failed_telegram_statuses(self, users):
        '''
        Создает объекты, хранящие информацию о пользователях, которым не удалось отправить email-сообщение
        '''

        failed_telegram_statuse1 = TelegramSendStatus.objects.create(user=users[0], is_successful=False)
        failed_telegram_statuses2 = TelegramSendStatus.objects.create(user=users[1], is_successful=False)

    @pytest.mark.django_db
    def test_successful_sms_send(self, mock_sms_aero, failed_telegram_statuses):
        mock_api = MagicMock()
        mock_api.send_sms.return_value = {"success", True}
        mock_sms_aero.return_value = mock_api

        send_sms_message('Test message')

        mock_sms_aero.assert_called_once_with(settings.SMSAERO_EMAIL, settings.SMSAERO_API_KEY)

        assert mock_api.send_sms.call_count == 2

        calls = mock_api.send_sms.call_args_list
        assert calls[0][0] == (79915410704, 'Test message')
        assert calls[1][0] == (79644111469, 'Test message')


def TestGenerateNotificationReport():
    pass
