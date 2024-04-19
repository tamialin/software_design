import os
import sys
import pytest
from unittest.mock import patch
import hashlib

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@pytest.fixture(scope="module")
def profile_user_data():
    return {
        'username': 'test_user',
        'password': hashlib.sha256('test_password'.encode()).hexdigest(),
        'fullname': 'Test User',
        'address1': '123 Test St',
        'address2': '',
        'city': 'Test City',
        'states': 'TS',
        'zip': '12345'
    }

@pytest.fixture
def logged_in_user(client, profile_user_data):
    """Log in a user for testing purposes."""
    with client.session_transaction() as session:
        session['username'] = profile_user_data['username']
        session['password'] = profile_user_data['password']

    with patch('app.mysql') as mysql_mock:
        cursor_mock = mysql_mock.connection.cursor.return_value
        cursor_mock.fetchone.return_value = (
            profile_user_data['username'],
            profile_user_data['password'],
            profile_user_data['fullname'],
            profile_user_data['address1'],
            profile_user_data['address2'],
            profile_user_data['city'],
            profile_user_data['states'],
            profile_user_data['zip']
        )

@pytest.fixture(scope="module")
def mysql(profile_user_data):
    with patch('app.mysql') as mysql_mock:
        cursor_mock = mysql_mock.connection.cursor.return_value
        cursor_mock.fetchone.return_value = (
            profile_user_data['username'],
            profile_user_data['password'],
            profile_user_data['fullname'],
            profile_user_data['address1'],
            profile_user_data['address2'],
            profile_user_data['city'],
            profile_user_data['states'],
            profile_user_data['zip']
        )
        yield mysql_mock
# # HOME ROUTES
# def test_home_route(client):
#     response = client.get('/')
#     assert response.status_code == 200
        
# HISTORY ROUTES
def test_access_history_when_logged_in(client, logged_in_user, mysql):
    response = client.get('/history', follow_redirects=True)
    assert response.status_code == 200
    assert b'Pricing Quote History' in response.data

def test_access_history_when_not_login(client):
    response = client.get('/history')
    assert response.status_code == 302 # successfully redirected
    assert '/login/history' in response.headers['Location']

# QUOTE ROUTES
def test_access_quote_when_logged_in(client, logged_in_user, profile_user_data):
    response = client.get('/quote', follow_redirects=True)
    print(response.text)
    assert response.status_code == 200
    assert profile_user_data['address1'].encode() in response.data
    assert b'Make a Quote' in response.data
def test_quote_page_when_not_login(client):
    response = client.get('/quote')
    assert response.status_code == 302 # successfully redirected
    assert '/login/quote' in response.headers['Location'] # Check if redirected to login route with 'quote' as clickfrom


# PROFILE ROUTES
def test_access_profile_when_logged_in(client, logged_in_user, profile_user_data):
    response = client.get('/profile', follow_redirects=True)
    assert response.status_code == 200
    assert profile_user_data['fullname'].encode() in response.data
    assert profile_user_data['address1'].encode() in response.data
def test_access_profile_when_not_login(client):
    response = client.get('/profile')
    assert response.status_code == 302 # successfully redirected
    assert '/login/profile' in response.headers['Location']

# LOGOUT ROUTES
def test_logout(client):
    # Set up a session with a logged-in user
    with client.session_transaction() as session:
        session['username'] = 'test_user'
    response = client.get('/logout', follow_redirects=True)
    # Assert that the response redirects to the home page
    assert response.status_code == 200
    with client.session_transaction() as session:
        assert 'username' not in session

# REGISTER ROUTES
def test_register_get(client):
    response = client.get('/register')
    assert response.status_code == 200
    # Assert that the response contains the registration form
    assert b'<form action="/register", method="POST" onsubmit="return registerAccount()">' in response.data

def test_register_post(client, mysql):
    # Make a POST request to /register with valid form data
    response = client.post('/register', data={
        'username': 'test_user',
        'password': 'test_password',
        're-password': 'test_password'  # Ensure the re-entered password matches
    }, follow_redirects=True)
    assert response.status_code == 200 # OK