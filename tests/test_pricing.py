# unit test for getting price in quote page
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