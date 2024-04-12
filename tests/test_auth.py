# unit test for login page
import os
import sys
import pytest

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from utils.pricing import FuelPricing

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login_success1(client):
    response = client.post('/login', data=dict(username='user1', password='password1'), follow_redirects=True)
    assert response.status_code == 200
    assert b"FUEL QUOTE" in response.data

def test_login_failure1(client):
    response = client.post('/login', data=dict(username='user1', password='wrong_password'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password. Please try again." in response.data
    
def test_login_success2(client):
    response = client.post('/login', data=dict(username='user2', password='password2'), follow_redirects=True)
    assert response.status_code == 200
    assert b"FUEL QUOTE" in response.data

def test_login_failure2(client):
    response = client.post('/login', data=dict(username='user2', password='wrong_password'), follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid username or password. Please try again." in response.data