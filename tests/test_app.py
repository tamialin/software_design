import os
import sys
import pytest
import json

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from utils.pricing import FuelPricing

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

# unit test for login page
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

# unit test for quote page
def test_quote_form_present(client):
    response = client.get('/quote')
    assert b"Make a Quote" in response.data
    assert b"Gallons Requested" in response.data
    assert b"Delivery Address" in response.data
    assert b"Delivery Date" in response.data

def test_quote_form_submission(client):
    response = client.post('/quote', data={'gallonsRequested': '100', 'deliveryDate': '2024-03-28'}, follow_redirects=True)
    assert response.status_code == 200
    # Parse JSON response
    response_data = json.loads(response.data)
    # Check if the expected keys are present
    assert 'suggested_price' in response_data
    assert 'total_price' in response_data

def test_fuel_pricing1():
    fuel_pricing = FuelPricing()
    suggested_price, total_price = fuel_pricing.calculatingPrice(100)
    assert suggested_price == 0.26  # Assuming calculations are correct
    assert total_price == 26.0  # Assuming calculations are correct

def test_fuel_pricing2():
    fuel_pricing = FuelPricing()
    suggested_price, total_price = fuel_pricing.calculatingPrice(1500)
    assert suggested_price == 0.24  # Assuming calculations are correct
    assert total_price == 360.0

def test_fuel_pricing_return_customer():
    fuel_pricing = FuelPricing()
    suggested_price, total_price = fuel_pricing.calculatingPrice(100, return_customer=True)
    assert suggested_price == 0.24  # Assuming calculations are correct with return customer
    assert total_price == 24  # Assuming calculations are correct with return customer