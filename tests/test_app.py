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
        
# unit test for loading each page:
def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"FUEL QUOTE" in response.data

def test_about_page(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b"About Us" in response.data
    
# Function to simulate login
def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)

# login and without login:
def test_quote_page(client):
    with client.session_transaction() as sess:
        sess['username'] = None  # Simulate not logged in
    response = client.get('/quote')
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'
    
def test_quote_page_login(client):
    # Simulate login
    login_response = login(client, 'user1', 'password1')
    assert login_response.status_code == 200  # Ensure login was successful
    response = client.get('/quote')
    assert response.status_code == 200
    assert b"Make a Quote" in response.data
    assert b"Gallons Requested" in response.data
    assert b"Delivery Address" in response.data
    assert b"Delivery Date" in response.data

def test_history_page(client):
    with client.session_transaction() as sess:
        sess['username'] = None
    response = client.get('/history')
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'
    
def test_history_page_login(client):
    login_response = login(client, 'user1', 'password1')
    assert login_response.status_code == 200
    response = client.get('/history')
    assert response.status_code == 200
    assert b"History" in response.data
    
def test_profile_page(client):
    with client.session_transaction() as sess:
        sess['username'] = None
    response = client.get('/profile')
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'
    
def test_profile_page_login(client):
    login_response = login(client, 'user1', 'password1')
    assert login_response.status_code == 200
    response = client.get('/profile')
    assert response.status_code == 200
    assert b"My Profile" in response.data

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_register_page(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data