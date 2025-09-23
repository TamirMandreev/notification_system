from notifications.models import User


def create_users(users):
    for user in users:
        User.objects.create(name=user[0], email=user[1], number=user[2])

