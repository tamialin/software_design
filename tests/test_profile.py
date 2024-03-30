import os
import sys
import pytest

# Add the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from utils.temp_db import users_db

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_default_profile_values(client):
    with client.session_transaction() as sess:
        sess['username'] = 'user1'  # Assuming user1 is logged in

        response = client.get('/profile')
        assert response.status_code == 302

        # Check if default values are displayed in the form
        assert b'value="John Doe"' in response.data
        assert b'value="1314 Shadowbrook St"' in response.data
        assert b'value="Anytown"' in response.data
        assert b'value="CA"' in response.data
        assert b'value="12345"' in response.data

# def test_profile_update(client):
#     with client.session_transaction() as sess:
#         sess['username'] = 'user1'

#         # Simulate form submission with updated values
#         data = {
#             'fullname': 'New Name',
#             'address1': 'New Address 1',
#             'address2': 'New Address 2',
#             'city': 'New City',
#             'states': 'NY',
#             'zip': '54321'
#         }
#         response = client.post('/profile', data=data, follow_redirects=True)
#         assert response.status_code == 200

#         # Check if the profile is updated in the database
#         assert 'user1' in users_db
#         assert users_db['user1']['fullname'] == 'New Name'
#         assert users_db['user1']['address1'] == 'New Address 1'
#         assert users_db['user1']['address2'] == 'New Address 2'
#         assert users_db['user1']['city'] == 'New City'
#         assert users_db['user1']['states'] == 'NY'
#         assert users_db['user1']['zip'] == '54321'

