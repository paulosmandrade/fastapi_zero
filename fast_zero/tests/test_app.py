from fast_zero.schemas import UserPublic


def test_root_deve_retornar_200_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == 200
    assert response.json() == {'message': 'Olá Mundo!'}


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'paulo',
            'email': 'paulo@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 201
    assert response.json() == {
        'email': 'paulo@example.com',
        'username': 'paulo',
        'id': 1,
    }


def test_create_user_error_400_username_alredy_registered(client, user):
    response = response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'email': 'teste@test.com',
            'password': 'testtest',
        },
    )

    assert response.status_code == 400
    assert response.json() == {'detail': 'Username alredy registered'}


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == {'users': []}


def test_read_users_with_users(user):
    user_schema = UserPublic.model_validate(user).model_dump()
    assert {
        'users': [{'email': 'teste@test.com', 'id': 1, 'username': 'Teste'}]
    } == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'mynewpassword',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'username': 'bob',
        'email': 'bob@example.com',
        'id': 1,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_erro_update_user_400_not_permission(client, token):
    response = client.put(
        '/users/100000000',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'Fernanda',
            'email': 'fernanda@exemplo.com.br',
            'password': '123456',
        },
    )
    assert response.status_code == 400


def test_erro_delete_user_401_not_permission(client):
    response = client.delete('/users/1000')

    assert response.status_code == 401


def test_retorna_usuario_especifico(client):
    response = client.post(
        '/users/',
        json={
            'username': 'paulo',
            'email': 'paulo@example.com',
            'password': 'secret',
        },
    )
    assert response.status_code == 201

    response = client.get('/users/1')

    assert response.status_code == 200


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )
    token = response.json()

    assert response.status_code == 200
    assert 'access_token' in token
    assert 'token_type' in token
