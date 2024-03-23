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


def test_update_user(client, user):
    response = client.put(
        '/users/1',
        json={
            'username': 'Bernardo',
            'email': 'bernardo@example.com.br',
            'password': 'ratunamatata',
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        'username': 'Bernardo',
        'email': 'bernardo@example.com.br',
        'id': 1,
    }


def test_delete_user(client, user):
    response = client.delete('/users/1')

    assert response.status_code == 200
    assert response.json() == {'message': 'User deleted'}


def test_erro_update_user_404_not_found(client):
    response = client.put(
        '/users/1000',
        json={
            'username': 'Fernanda',
            'email': 'fernanda@exemplo.com.br',
            'password': '123456',
        },
    )
    assert response.status_code == 404


def test_erro_delete_user_404_not_found(client, user):
    response = client.delete('/users/1000')

    assert response.status_code == 404


def test_retorna_usuario_especifico(client, user):
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
