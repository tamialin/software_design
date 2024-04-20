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
        
def test_register_user(client):
    mock_mysql = Mock()
    mock_cursor = mock_mysql.connection.cursor.return_value
    mock_cursor.fetchone.return_value = None 

    mock_session = {}
    with patch('utils.register.session', mock_session):
        form_data = {'username': 'test_user', 'password': 'password', 're-password': 'password'}
        with app.test_request_context('/', method='POST', data = form_data):
            result = register_user(mock_mysql)
            assert 'User registered successfully!' in result
            assert mock_cursor.execute.called
            assert mock_mysql.connection.commit.called
            assert mock_cursor.close.called
            assert mock_session['username'] == 'test_user'

def test_username_already_exists(client):
    mock_mysql = Mock()
    mock_cursor = mock_mysql.connection.cursor.return_value
    mock_cursor.fetchone.return_value = ('test_user', 'hashed_password')

    mock_session = {}
    with patch('utils.register.session', mock_session):
        form_data = {'username': 'test_user', 'password': 'password', 're-password': 'password'}
        with app.test_request_context('/', method='POST', data=form_data):
            result = register_user(mock_mysql)
            assert 'Username already exists.' in result

def test_password_mismatch(client):
    mock_mysql = Mock()
    form_data = {'username': 'test_user', 'password': 'password', 're-password': 'different_password'}
    with app.test_request_context('/', method='POST', data=form_data):
        result = register_user(mock_mysql)
        assert 'Password and Re-enter Password must be the same' in result

def test_database_commit_failure(client):
    mock_mysql = Mock()
    mock_cursor = mock_mysql.connection.cursor.return_value
    mock_cursor.execute.side_effect = Exception("Database commit failed")

    with pytest.raises(Exception) as e:
        form_data = {'username': 'test_user', 'password': 'password', 're-password': 'password'}
        with app.test_request_context('/', method='POST', data=form_data):
            register_user(mock_mysql)
    
    assert str(e.value) == "Database commit failed"

def test_edge_cases_username_password(client):
    mock_mysql = Mock()
    mock_cursor = mock_mysql.connection.cursor.return_value
    mock_cursor.fetchone.return_value = None

    test_cases = [
        {'username': '', 'password': 'password', 're-password': 'password'},  # Empty username
        {'username': 'test_user!', 'password': 'password', 're-password': 'password'},  # Username with special characters
        {'username': 'test_user', 'password': 'password!', 're-password': 'password!'},  # Password with special characters
    ]

    for form_data in test_cases:
        with app.test_request_context('/', method='POST', data=form_data):
            result = register_user(mock_mysql)
            assert 'User registered successfully!' in result
            assert mock_cursor.execute.called
            assert mock_mysql.connection.commit.called
            assert mock_cursor.close.called
