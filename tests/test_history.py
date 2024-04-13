# unit test for profile page
import os
import sys
import pytest

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import session
from app import app
from utils.pricing import FuelPricing
from utils.history import get_quote_history
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

def test_get_quote_history(mocker):
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        (1, 'username', '2023-01-01', 100, '123 Main St', 1.23, 123.45),
        (2, 'username', '2023-02-01', 200, '456 Elm St', 2.34, 234.56)
    ]
    mock_mysql = mocker.Mock()
    mock_mysql.connection.cursor.return_value = mock_cursor
    quote_history = get_quote_history('username', mock_mysql)

    assert quote_history == [
        (1, 'username', '2023-01-01', 100, '123 Main St', 1.23, 123.45),
        (2, 'username', '2023-02-01', 200, '456 Elm St', 2.34, 234.56)
    ]
