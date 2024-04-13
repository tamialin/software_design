import os
import sys
from unittest import mock

import pytest

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from utils.register import register_user  # Import your register_user function
from unittest.mock import Mock, patch
from flask import render_template, request

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        
@mock.patch('utils.register')
def test_register_user(mocker):
    # Mocking MySQL connection and cursor
    mock_mysql = Mock()
    mock_cursor = mocker.Mock()
    mock_mysql.connection.cursor.return_value = mock_cursor

    # Mocking execute method of the cursor
    mock_cursor.fetchone.return_value = None  # No user with the same username exists
    mock_cursor.fetchall.return_value = None  # Mocking an empty result for select query

    # Mocking session object
    mock_session = {}
    mocker.patch('utils.register.session', mock_session)

    # Mocking form data
    form_data = {'username': 'test_user', 'password': 'password', 're-password': 'password'}
    with patch('utils.register.request.form', return_value="Testing"):
        result = register_user()
        yield result
    # mocker.patch('utils.register.request.form', form_data)
        

    # Calling the function
    result = register_user(mock_mysql)

    # Asserting the expected behavior
    assert result == render_template('register.html', success_message='User registered successfully!')
    mock_cursor.execute.assert_called_once_with("INSERT INTO users (username, password) VALUES (%s, %s)", ('test_user', '5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8'))  # Ensure password hashing is correct
    mock_mysql.connection.commit.assert_called_once()
    mock_cursor.close.assert_called_once()

    # Testing for existing username
    mock_cursor.fetchone.return_value = ('test_user', 'hashed_password')  # Mocking an existing user
    result = register_user(mock_mysql)