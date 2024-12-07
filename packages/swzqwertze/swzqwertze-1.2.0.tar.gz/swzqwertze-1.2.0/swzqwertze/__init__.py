def sum(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract b from a."""
    return a - b

def multiply(a, b):
    """Multiply two numbers."""
    return a * b

def divide(a, b):
    """Divide a by b. Raises ZeroDivisionError if b is 0."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b

def power(a, b):
    """Raise a to the power of b."""
    return a ** b

def modulo(a, b):
    """Return remainder of a divided by b."""
    if b == 0:
        raise ZeroDivisionError("Cannot calculate modulo with zero")
    return a % b

def floor_divide(a, b):
    """Floor division of a by b."""
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a // b

def absolute(a):
    """Return absolute value of a number."""
    return abs(a)
