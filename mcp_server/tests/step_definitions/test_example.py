import pytest
from pytest_bdd import scenarios, given, when, then

# Feature 파일 연결
scenarios("../features/example.feature")

# Fixture 정의
@pytest.fixture
def account_balance():
    return {"balance": 100}

# Given
@given("the account balance is $100")
def step_given_balance(account_balance):
    account_balance["balance"] = 100

# When
@when("I deposit $20")
def step_when_deposit(account_balance):
    account_balance["balance"] += 20

# Then
@then("the account balance should be $120")
def step_then_check_balance(account_balance):
    assert account_balance["balance"] == 120
