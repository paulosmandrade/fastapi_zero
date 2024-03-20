import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_deve_retornar_200_e_ola_mundo(client):

    response = client.get('/')

    assert response.status_code == 200


def test_create_user(client):
    client = TestClient(app)

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
        'username': 'paulo',
        'email': 'paulo@example.com',
        'id': 1,
    }


def test_read_users(client):
    response = client.get('/users/')
    assert response.status_code == 200
    assert response.json() == {
        'users': [
            {
                'username': 'paulo',
                'email': 'paulo@example.com',
            }
        ]
    }
