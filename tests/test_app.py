from http import HTTPStatus


def test_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')  # Act

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}  # Assert


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'testusername',
            'email': 'test@test.com',
            'password': 'password',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'testusername',
        'email': 'test@test.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'testusername',
                'email': 'test@test.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
        json={
            'password': '123456',
            'username': 'testusername2',
            'email': 'test@test.com',
            'id': 1,
        },
    )

    assert response.json() == {
        'username': 'testusername2',
        'email': 'test@test.com',
        'id': 1,
    }


def test_id_read_user(client):
    response = client.get('/users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'testusername2',
                'email': 'test@test.com',
                'id': 1,
            }
        ]
    }


def test_delete_user(client):
    reponse = client.delete('/users/1')

    assert reponse.json() == {'message': 'User deleted'}


def test_id_user_invalid(client):
    response_update = client.put(
        '/users/100000',
        json={
            'password': '123456',
            'username': 'testusername2',
            'email': 'test@test.com',
            'id': 1,
        },
    )

    response_delete = client.delete('/users/100000')

    assert response_update.status_code == HTTPStatus.NOT_FOUND
    assert response_delete.status_code == HTTPStatus.NOT_FOUND
