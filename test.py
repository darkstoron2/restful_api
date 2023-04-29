from requests import get, post, delete
from data.user_resource import UserResource, UserListResource


def test():
    # Правильные запросы
    """
    print(get('http://localhost:5000/api/v2/user').json())

    print(get('http://localhost:5000/api/v2/user/1').json())

    print(post('http://localhost:5000/api/v2/user', json=
    {
        'name': 'Slava',
        'surname': 'SurSlava',
        'age': 16,
        'email': 'slavasur@gmail.com',
        'password': 'password'
    }).json())
    print(get('http://localhost:5000/api/v2/user').json())

    print(delete('http://localhost:5000/api/v2/user/6').json())
    print(get('http://localhost:5000/api/v2/user').json())
    """
    print(get('http://localhost:5000/api/v2/user/999'))  # Нет такого пользователя
    print(post('http://localhost:5000/api/v2/user', json={}).json())  # Нет ключей
    print(delete('http://localhost:5000/api/v2/user/999'))  # Нет такого пользователя


test()
