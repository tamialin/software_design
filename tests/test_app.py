import os
import sys
import pytest

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"FUEL QUOTE" in response.data

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About Us" in response.data

def test_quote_page(client):
    response = client.get('/quote')
    assert response.status_code == 200
    assert b"Make a Quote" in response.data

def test_history_page(client):
    response = client.get('/history')
    assert response.status_code == 200
    assert b"History" in response.data

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_login_success1(client):
    response = client.post('/login', data=dict(username='user1', password='password1'), follow_redirects=True)
    assert response.status_code == 200
    assert b"My Profile" in response.data

def test_login_failure1(client):
    response = client.post('/login', data=dict(username='user1', password='wrong_password'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password. Please try again." in response.data
    
def test_login_success2(client):
    response = client.post('/login', data=dict(username='user2', password='password2'), follow_redirects=True)
    assert response.status_code == 200
    assert b"My Profile" in response.data

def test_login_failure2(client):
    response = client.post('/login', data=dict(username='user2', password='wrong_password'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password. Please try again." in response.data
