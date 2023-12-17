# tests/test_auth.py

import pytest
from app import app, db

@pytest.fixture
def authenticated_client():
    # Assuming you have a login route that logs in a user
    client = app.test_client()
    client.post('/login', data=dict(username='testuser', password='password'))
    return client

def test_authenticated_route(authenticated_client):
    response = authenticated_client.get('/authenticated_route')
    assert b'Welcome, testuser!' in response.data
