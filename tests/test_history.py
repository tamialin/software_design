# unit test for profile page
import os
import sys
import pytest
import json

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from utils.pricing import FuelPricing
from utils.history import update_quote_history, get_quote_history

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
        
# def test_quote_form_submission(client):
    # response = client.post('/quote', data={'gallonsRequested': '100', 'deliveryDate': '2024-03-28'}, follow_redirects=True)
    # assert response.status_code == 200
    # # Parse JSON response
    # response_data = json.loads(response.data)
    # # Check if the expected keys are present
    # assert 'suggested_price' in response_data
    # assert 'total_price' in response_data
    
def test_quote_form_submission(client):
    # Simulating a POST request to the fuel quote endpoint
    response = client.post('/quote', data={
        'gallonsRequested': '100',
        'deliveryDate': '2024-04-01'
    })

    # Check if the response status code is 200 (success)
    assert response.status_code == 302

    # Check if the response contains suggested_price and total_price
    data = response.json
    assert 'suggested_price' in data
    assert 'total_price' in data

def test_update_quote_history():
    # Test case for updating quote history for a user
    username = 'user1'
    quote_data = {
        'delivery_date': '2024-04-01',
        'gallon_requested': 100,
        'suggested_price': 0.26,
        'total_price': 26.0
    }
    assert update_quote_history(username, quote_data) == True

def test_get_quote_history():
    # Test case for getting quote history for a user
    username = 'user1'
    expected_history = [
        {
            'delivery_date': '2024-04-01',
            'gallon_requested': 100,
            'delivery_address': '123 Main St',
            'suggested_price': 0.26,
            'total_price': 26.0
        }
    ]
    assert get_quote_history(username) == expected_history