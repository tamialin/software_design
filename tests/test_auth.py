# unit test for login page
import os
import sys
import pytest
from unittest.mock import patch
import hashlib

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app
from flask import session


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.fixture
def mysql():
    # Mock the MySQL connection
    with patch('app.mysql') as mysql_mock:
        # Mock the connection.cursor() method
        cursor_mock = mysql_mock.connection.cursor.return_value
        # Mock the cursor.fetchone() method to return a sample user data
        cursor_mock.fetchone.return_value = ('test_user', 'hashed_password')
        yield mysql_mock       

# Test case for handle_login function
def test_handle_login_success(client, mysql):
    # Mock form data for a valid login attempt
    form_data_valid = {
    'username': 'test_user',
    'password': 'test_password',
}
    # Mock the MySQL cursor and execute method to simulate a successful authentication
    cursor_mock = mysql.connection.cursor.return_value
    cursor_mock.fetchone.return_value = ('test_user', hashlib.sha256('test_password'.encode()).hexdigest())

    # Send a POST request with valid form data to the login endpoint
    response = client.post('/login', data=form_data_valid, follow_redirects=True)

    # Ensure that the request was successful and redirected to the home page
    assert response.status_code == 200  # Assuming a successful login
    assert session.get("username") == 'test_user'  # Ensure session username is set to the correct value
    assert b'<title>FUEL QUOTE</title>' in response.data
    

def test_handle_login_failure0(client, mysql):
    form_data_invalid = {
        'username': 'invalid_user',
        'password': 'invalid_password'
    }
    cursor_mock = mysql.connection.cursor.return_value
    cursor_mock.fetchone.return_value = None
    response = client.post('/login', data=form_data_invalid, follow_redirects=True)
    assert response.status_code == 200  
    assert b"Invalid username or password. Please try again." in response.data
    assert b"Login" in response.data  

def test_handle_login_failure1(client, mysql):
    form_data_invalid = {
        'username': 'test_user',
        'password': 'invalid_password'
    }
    cursor_mock = mysql.connection.cursor.return_value
    cursor_mock.fetchone.return_value = ('test_user', hashlib.sha256('test_password'.encode()).hexdigest())
    response = client.post('/login', data=form_data_invalid, follow_redirects=True)
    
    assert response.status_code == 200  
    assert b"Invalid username or password. Please try again." in response.data
    assert b"Login" in response.data 
