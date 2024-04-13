# unit test for login page
import os
import sys
import pytest

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from unittest.mock import Mock, patch
from flask import session

# Import the function to be tested
from utils.auth import handle_login

# Define a fixture for the Flask app
@pytest.fixture
def app():
    from flask import Flask
    app = Flask(__name__, template_folder='templates')
    return app

# Define a mock MySQL connection object
@pytest.fixture
def mysql():
    return Mock()

def test_handle_login_valid(mysql, app):
    # Mock MySQL cursor object
    cursor_mock = mysql.connection.cursor.return_value
    # Mock the execute method of the cursor object
    cursor_mock.fetchone.return_value = ('test_user', 'hashed_password')

    # Mock Flask request context
    with app.test_request_context('/login.html', method='POST', data={'username': 'test_user', 'password': 'test_password'}):
        # Call the handle_login function
        with patch('utils.auth.redirect', side_effect=lambda url: url) as redirect_mock:
            result = handle_login(mysql)
            assert session['username'] == 'test_user'
            assert result == '/home'  # Assuming redirect to home page

            # Assert that the redirect function was called with the correct URL
            redirect_mock.assert_called_once_with('/home')

def test_handle_login_invalid(mysql, app):
    # Mock MySQL cursor object
    cursor_mock = mysql.connection.cursor.return_value
    # Mock the execute method of the cursor object
    cursor_mock.fetchone.return_value = None

    # Mock Flask request context
    with app.test_request_context('/login', method='POST', data={'username': 'test_user', 'password': 'test_password'}):
        # Call the handle_login function
        result = handle_login(mysql)
        assert 'username' not in session
        assert 'Invalid username or password' in result  # Assuming rendering login page with error message


# def test_login_success1(client):
#     response = client.post('/login', data=dict(username='user1', password='password1'), follow_redirects=True)
#     assert response.status_code == 200
#     assert b"FUEL QUOTE" in response.data

# def test_login_failure1(client):
#     response = client.post('/login', data=dict(username='user1', password='wrong_password'), follow_redirects=True)
#     assert response.status_code == 200
#     assert b"Invalid username or password. Please try again." in response.data
    
# def test_login_success2(client):
#     response = client.post('/login', data=dict(username='user2', password='password2'), follow_redirects=True)
#     assert response.status_code == 200
#     assert b"FUEL QUOTE" in response.data

# def test_login_failure2(client):
#     response = client.post('/login', data=dict(username='user2', password='wrong_password'), follow_redirects=True)
#     assert response.status_code == 200
#     assert b"Invalid username or password. Please try again." in response.data

