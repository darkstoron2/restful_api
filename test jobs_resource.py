from requests import get, post, delete, put


def test():
    # Правильные запросы
    print(get('http://localhost:5000/api/v2/jobs').json())

    print(get('http://localhost:5000/api/v2/jobs/1').json())

    print(post('http://localhost:5000/api/v2/jobs', json={
        'team_leader': 1,
        'job': 'SomeJob',
        'work_size': 16,
        'is_finished': True
    }).json())
    print(get('http://localhost:5000/api/v2/jobs').json())

    print(delete('http://localhost:5000/api/v2/jobs/2').json())
    print(get('http://localhost:5000/api/v2/jobs').json())

    print(put('http://localhost:5000/api/v2/jobs/1', json={
        'job': 'NewNewJob'
    }).json())
    print(get('http://localhost:5000/api/v2/jobs/1').json())

    print(get('http://localhost:5000/api/v2/jobs/999'))  # Нет такой работы
    print(post('http://localhost:5000/api/v2/jobs', json={}).json())  # Нет ключей
    print(delete('http://localhost:5000/api/v2/jobs/999'))  # Нет такой работы


test()
