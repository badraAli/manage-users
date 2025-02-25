import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == 200
    assert response.json == []

def test_create_user(client):
    response = client.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
    assert response.status_code == 201
    assert response.json['username'] == 'testuser'
    assert response.json['email'] == 'test@example.com'

def test_update_user(client):
    client.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
    response = client.put('/users/1', json={'username': 'updateduser', 'email': 'updated@example.com'})
    assert response.status_code == 200
    assert response.json['username'] == 'updateduser'
    assert response.json['email'] == 'updated@example.com'

def test_delete_user(client):
    client.post('/users', json={'username': 'testuser', 'email': 'test@example.com'})
    response = client.delete('/users/1')
    assert response.status_code == 204
    response = client.get('/users/1')
    assert response.status_code == 404