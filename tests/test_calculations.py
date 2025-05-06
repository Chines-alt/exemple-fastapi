import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount

@pytest.fixture
def zero_bank_account():
    """Fixture to create a BankAccount with zero balance."""
    return BankAccount(0)

@pytest.fixture
def bank_account():
    """Fixture to create a BankAccount with a specific balance."""
    return BankAccount(1000)

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 3),
    (5, 3, 8),
    (10, 20, 30),
])
def test_add_parametrized(num1, num2, expected):
    assert add(num1, num2) == expected

def test_add():
    assert add(5, 3) == 8
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
    assert add(-1, -1) == -2
    assert add(1000000, 1000000) == 2000000

def test_subtract():
    assert subtract(5, 3) == 2
    assert subtract(0, 0) == 0
    assert subtract(-1, -1) == 0
    assert subtract(1000000, 500000) == 500000

def test_multiply():
    assert multiply(5, 3) == 15
    assert multiply(0, 5) == 0
    assert multiply(-1, -1) == 1
    assert multiply(1000000, 1000000) == 1000000000000

def test_divide():
    assert divide(6, 3) == 2
    assert divide(0, 1) == 0
    assert divide(-6, -3) == 2
    assert divide(1000000, 1000000) == 1
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)

def test_bank_set_initial_balance(zero_bank_account):
    """Test the initial balance of the bank account."""
    assert zero_bank_account.balance == 0

def test_bank_account():
    account = BankAccount(1000)
    assert account.balance == 1000

    account.deposit(500)
    assert account.balance == 1500

    account.withdraw(200)
    assert account.balance == 1300

    account.collect_interest(0.05)
    assert account.balance == 1365.0

    with pytest.raises(ValueError):
        account.deposit(-100)

    with pytest.raises(ValueError):
        account.withdraw(2000)

    with pytest.raises(ValueError):
        account.collect_interest(-0.05)

def test_withdraw():
    account = BankAccount(1000)
    account.withdraw(200)
    assert account.balance == 800

    with pytest.raises(ValueError):
        account.withdraw(1000)

    with pytest.raises(ValueError):
        account.withdraw(-100)

def test_collect_interest():
    account = BankAccount(1000)
    account.collect_interest(0.05)
    assert account.balance == 1050.0

    with pytest.raises(ValueError):
        account.collect_interest(-0.05)

    with pytest.raises(ValueError):
        account.collect_interest(0)


def test_bank_transactions():
    account = BankAccount(1000)
    account.deposit(500)
    assert account.balance == 1500

    account.withdraw(200)
    assert account.balance == 1300

    account.collect_interest(0.05)
    assert account.balance == 1365.0

    with pytest.raises(ValueError):
        account.deposit(-100)

    with pytest.raises(ValueError):
        account.withdraw(2000)

    with pytest.raises(ValueError):
        account.collect_interest(-0.05)

def test_bank_account_fixture(bank_account):
    """Test the bank account fixture."""
    assert bank_account.balance == 1000

    bank_account.deposit(500)
    assert bank_account.balance == 1500

    bank_account.withdraw(200)
    assert bank_account.balance == 1300

    bank_account.collect_interest(0.05)
    assert bank_account.balance == 1365.0

    with pytest.raises(ValueError):
        bank_account.deposit(-100)

    with pytest.raises(ValueError):
        bank_account.withdraw(2000)

    with pytest.raises(ValueError):
        bank_account.collect_interest(-0.05)

def test_collect_interest():
    account = BankAccount(1000)
    account.collect_interest(0.05)
    assert account.balance == 1050.0

    with pytest.raises(ValueError):
        account.collect_interest(-0.05)

    with pytest.raises(ValueError):
        account.collect_interest(0)

def test_insufficient_funds():
    account = BankAccount(1000)
    with pytest.raises(ValueError):
        account.withdraw(2000)