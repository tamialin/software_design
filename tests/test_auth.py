import pytest
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        
def test_handle_login(client):
    response = client.post('/login', data=dict(username='user1', password='password1'), follow_redirects=True)
    assert response.status_code == 200
    assert b"My Profile" in response.data
    # assert b"Login" in response.data
    
def test_login_failure1(client):
    response = client.post('/login', data=dict(username='user1', password='wrong_password'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password. Please try again." in response.data