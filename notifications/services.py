from notifications.models import User
from notifications.tasks import send_async_email

def create_users(users):
    for user in users:
        User.objects.create(name=user[0], email=user[1], number=user[2])


def send_users_email(subject, message,):
    '''
    Отправляет каждому пользователю письмо
    :param subject: str: Тема письма
    :param message: str: Текст письма
    '''
    users = User.objects.all()
    for user in users:
        send_async_email.delay(subject, message, user.id, user.email)

