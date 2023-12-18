import json
import pytest
from app import app, db
from app.models import User, RedFlag, Intervention, AdminAction

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

def logout(client):
    return client.get('/logout', follow_redirects=True)

def test_register(client):
    response = client.post('/register', data=dict(
        username='testuser',
        name='Test User',
        phone='1234567890',
        email='test@example.com',
        password='testpassword'
    ), follow_redirects=True)

    assert b'Your account has been created!' in response.data

def test_login_logout(client):
    test_register(client)

    response = login(client, 'test@example.com', 'testpassword')
    assert b'Login unsuccessful' not in response.data

    response = logout(client)
    assert b'You have been logged out' in response.data

def test_home_page(client):
    response = client.get('/')
    assert b'redflag_posts' in response.data
    assert b'intervention_posts' in response.data

# Add more tests for other routes as needed

if __name__ == '__main__':
    pytest.main()
