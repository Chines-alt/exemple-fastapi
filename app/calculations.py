def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

class BankAccount:
    def __init__(self, balance: float):
        self.balance = balance

    def deposit(self, amount: float):
        if amount > 0:
            self.balance += amount
        else:
            raise ValueError("Deposit amount must be positive")

    def withdraw(self, amount: float):
        if 0 < amount <= self.balance:
            self.balance -= amount
        else:
            raise ValueError("Withdrawal amount must be positive and less than or equal to the balance")

    def collect_interest(self, rate: float):
        if rate > 0:
            self.balance += self.balance * rate
        else:
            raise ValueError("Interest rate must be positive")

