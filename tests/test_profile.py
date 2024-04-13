import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

mysql_mock = MagicMock()
cursor_mock = MagicMock()
cursor_mock.fetchone.return_value = ('user1', 'password1', 'John Doe', '1314 Shadowbrook St', '', 'Anytown', 'CA', '12345', 'None')
mysql_mock.connection.cursor.return_value = cursor_mock

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_default_profile_values(client):
    with patch('app.mysql', mysql_mock):
        with client.session_transaction() as sess:
            sess['username'] = 'user1'  # Assuming user1 is logged in

        response = client.get('/profile')
        assert response.status_code == 200

        response = client.post('/profile', data={
            'fullname': 'Updated Name',
            'address1': 'Updated Address1', 
            'address2': 'Updated Address2', 
            'city': 'Updated City', 
            'states': 'Updated State', 
            'zip': 'Updated Zipcode'
            }, follow_redirects=True)
        assert response.status_code == 200

        # Check if default values are displayed in the form
        assert b'value="John Doe"' in response.data
        assert b'value="1314 Shadowbrook St"' in response.data
        assert b'value="Anytown"' in response.data
        assert b'value="CA"' in response.data
        assert b'value="12345"' in response.data