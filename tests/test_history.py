# unit test for profile page
import json
import os
import sys
import pytest
from unittest.mock import Mock, patch

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from utils.history import get_quote_history
from utils.fuelModule import fuelQuote

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

@pytest.mark.parametrize('submitter_id', ['getQuote', 'submitBtn'])
def test_quote_form_submission(client, mocker, submitter_id):
    # Mock fuelQuote function to return expected data
    mocker.patch('app.fuelQuote').return_value = {
        'suggested_price': 1.5,
        'total_price': 150
    }

    # Simulate form submission
    with client.session_transaction() as sess:
        sess['username'] = 'user1'
    response = client.post('/quote', data={
        'gallonsRequested': 100,
        'deliveryDate': '2024-04-01'
    })

    # Check if the form submission was successful
    assert response.status_code == 200

    # Check if the response contains expected JSON data
    json_data = response.get_json()
    assert 'suggested_price' in json_data
    assert 'total_price' in json_data

    # Check if the session is set properly
    with client.session_transaction() as sess:
        assert sess['username'] == 'user1'

    # Check if the AJAX request data matches the expected format
    #assert json_data['displayData'] == (submitter_id == 'getQuote')

    # Ensure that the submit button message is in the response content
    #assert '<p>Data successfully sent</p>' in response.get_data(as_text=True)


    
# def test_quote_form_submission(client):
#     # Test with user1
#     with client.session_transaction() as sess:
#         sess['username'] = 'user1'
        
#     # Simulate a POST request to the fuelQuote route
#     response = client.post('/quote', data=dict(
#         gallonsRequested=100,
#         deliveryDate='2024-04-01'
#     ))

#     # Check if the response is successful
#     assert response.status_code == 200

#     # Check if the quote history is updated for the user
#     assert 'username' in session  # Assuming session is set properly
#     username = session['username']
#     assert username in quote_history_db
#     assert len(quote_history_db[username]) == 1

#     # Check if the quote data matches the submitted data
#     quote_data = quote_history_db[username][0]
#     assert quote_data['gallon_requested'] == 100
#     assert quote_data['delivery_date'] == '2024-04-01'

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

# def test_send_to_db(client, mocker):
#     # Mock MySQL connection and cursor
#     mock_cursor = MagicMock()
#     mock_connection = MagicMock()
#     mock_connection.cursor.return_value = mock_cursor
#     mock_mysql = MagicMock()
#     mock_mysql.connection = mock_connection

#     with client.session_transaction() as sess:
#         sess['username'] = 'test_user@gmail'
        
#     mock_cursor.fetchone.return_value = ('test_user@gmail',)
        
#     # # Mock session username
#     # mocker.patch('flask.session.get').return_value = 'test_user@gmail'

#     # Call the function
#     sendToDB(mock_mysql, 'test_user@gmail', '2024-04-01', 100, '123 Main St', 1.5, 150)

#     # Assert that the correct SQL queries are executed with the correct parameters
#     mock_cursor.execute.assert_any_call(
#         "SELECT * FROM users WHERE username = %s", ('test_user@gmail',)
#     )
#     mock_cursor.execute.assert_any_call(
#         "INSERT INTO quote_history (username, date, gallon, address, price, total) VALUES (%s, %s, %s, %s, %s, %s)",
#         ('test_user@gmail', '2024-04-01', 100, '123 Main St', 1.5, 150)
#     )
#     mock_connection.commit.assert_called_once()

def test_get_quote():
    mock_mysql = Mock()
    # Mocking the cursor directly
    mock_cursor = mock_mysql.connection.cursor.return_value
    # Ensuring mock_cursor is returned when cursor() is called
    mock_cursor.fetchone.return_value = ['1314 Shadowbrook St', 'Houston', 'WA', '11111', True]

    mock_session = {'username': 'test_user'}
    with patch('utils.fuelModule.session', mock_session):
        form_data = {'gallonsRequested': '100', 'deliveryDate': '2024-04-18', 'displayData': 'true'}
        with app.test_request_context('/quote', method='POST', data = form_data):
            result = fuelQuote(mock_mysql)
            data = result.get_json()
            assert 'suggested_price' in data
            assert 'total_price' in data
            assert mock_session['username'] == 'test_user'
            
def test_submit():
    mock_mysql = Mock()
    mock_cursor = Mock()
    mock_mysql.connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ['1314 Shadowbrook St', 'Houston', 'WA', '11111', True]

    mock_session = {'username': 'test_user'}
    with patch('utils.fuelModule.session', mock_session):
        form_data = {'gallonsRequested': '100', 'deliveryDate': '2024-04-18', 'sendData': 'true'}
        with app.test_request_context('/quote', method='POST', data=form_data):
            result = fuelQuote(mock_mysql)
            data = result.get_json()
            assert 'success' in data
            assert data['success']
            assert mock_session['username'] == 'test_user'