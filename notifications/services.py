def get_recipient_list(users):
    '''
    Из списка пользователей формата
    [
        ["Тамир", "tamirmandreev@mail.ru", "89915410704"],
        ["Тимур", "mandreevts@gmail.com", "+79644111469"],
    ]
    получает список email-адресов формата
    [tamirmandreev@mail.ru, mandreevts@gmail.com,]
    :param users: список пользователей
    :return:
    '''
    recipient_list = []
    for user in users:
        email = user[1]
        recipient_list.append(email)

    return recipient_list
