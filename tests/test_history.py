# unit test for profile page
import os
import sys
import pytest

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import session
from app import app
from utils.pricing import FuelPricing
from utils.history import update_quote_history, get_quote_history
from utils.temp_db import quote_history_db

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client
    
def test_quote_form_submission(client):
    # Test with user1
    with client.session_transaction() as sess:
        sess['username'] = 'user1'
        
    # Simulate a POST request to the fuelQuote route
    response = client.post('/quote', data=dict(
        gallonsRequested=100,
        deliveryDate='2024-04-01'
    ))

    # Check if the response is successful
    assert response.status_code == 200

    # Check if the quote history is updated for the user
    assert 'username' in session  # Assuming session is set properly
    username = session['username']
    assert username in quote_history_db
    assert len(quote_history_db[username]) == 1

    # Check if the quote data matches the submitted data
    quote_data = quote_history_db[username][0]
    assert quote_data['gallon_requested'] == 100
    assert quote_data['delivery_date'] == '2024-04-01'

def test_update_quote_history():
    username = 'user2'
    quote_data = {
        'delivery_date': '2024-04-01',
        'gallon_requested': 100,
        'delivery_address': 'Test Address',
        'suggested_price': 1.5,
        'total_price': 150
    }

    # Add quote data
    update_quote_history(username, quote_data)
    assert username in quote_history_db
    assert len(quote_history_db[username]) == 1
    assert quote_history_db[username][0] == quote_data

def test_get_quote_history():
    username = 'user2'
    quote_data = {
        'delivery_date': '2024-04-01',
        'gallon_requested': 100,
        'delivery_address': 'Test Address',
        'suggested_price': 1.5,
        'total_price': 150
    }

    # Add quote data
    quote_history_db[username] = [quote_data]

    history = get_quote_history(username)
    assert isinstance(history, list)
    assert len(history) == 1
    assert history[0] == quote_data