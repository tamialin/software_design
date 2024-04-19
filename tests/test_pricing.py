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
    suggested_price, total_price = fuel_pricing.calculatingPrice(100, "TX", 0)
    assert suggested_price == 1.725 # Assuming calculations are correct
    assert total_price == 172.50 # Assuming calculations are correct

def test_fuel_pricing2():
    fuel_pricing = FuelPricing()
    suggested_price, total_price = fuel_pricing.calculatingPrice(1500, "TX", 1)
    assert suggested_price == 1.695 # Assuming calculations are correct
    assert total_price == 2542.5

def test_fuel_pricing_return_customer():
    fuel_pricing = FuelPricing()
    suggested_price, total_price = fuel_pricing.calculatingPrice(100, "TX", 1)
    assert suggested_price == 1.71 # Assuming calculations are correct with return customer
    assert total_price == 171  # Assuming calculations are correct with return customer
