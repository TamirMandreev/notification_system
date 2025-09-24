from notifications.models import User
from notifications.tasks import send_async_email

def create_users(users):
    for user in users:
        User.objects.create(name=user[0], email=user[1], number=user[2], tg_chat_id=user[3])







