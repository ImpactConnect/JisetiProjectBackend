import pytest
from flask import json
from app import app, db
from app.models import User, RedFlag, Intervention, AdminAction
from flask_login import current_user
from flask_testing import TestCase

class TestApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_register_route(self):
        response = self.client.post('/register', data=dict(
            username='testuser',
            name='Test',
            phone='12345678901',
            email='test@example.com',
            password='password',
            confirm_password='password'
        ), follow_redirects=True)

        assert b'Your account has been created!' in response.data
        assert User.query.filter_by(username='testuser').first() is not None

    def test_login_route(self):
        user = User(username='testuser', first_name='Test', last_name='User', phone='12345678901',
                    email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        response = self.client.post('/login', data=dict(
            email='test@example.com',
            password='password',
        ), follow_redirects=True)

        assert b'Login unsuccessful. Please check email and password.' not in response.data
        assert current_user.is_authenticated

    def test_home_page_route(self):
        # Assuming you have some RedFlag and Intervention records in the database
        response = self.client.get('/')
        data = json.loads(response.data)

        assert 'redflag_posts' in data
        assert 'intervention_posts' in data
        # Add more assertions based on your expected response structure

    # Add more test cases for other routes

if __name__ == '__main__':
    pytest.main()
