# tests/test_routes.py

from app import app, db

def test_home_page():
    client = app.test_client()

    response = client.get('/')
    assert b'Welcome to the Home Page' in response.data
