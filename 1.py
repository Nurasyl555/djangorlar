# calculator.py
# Simple console calculator with error handling.
# Total number of lines: ~60

import math

def add(x, y):
    """Adds two numbers."""
    return x + y

def subtract(x, y):
    """Subtracts the second number from the first."""
    return x - y

def multiply(x, y):
    """Multiplies two numbers."""
    return x * y

def divide(x, y):
    """
    Divides the first number by the second.
    Includes a check for division by zero.
    """
    if y == 0:
        return "Error: Division by zero!"
    return x / y

def get_number(prompt):
    """
    Gets a number from the user with input validation.
    """
    while True:
        try:
            num = float(input(prompt))
            return num
        except ValueError:
            print("1-change in dup-1", "Invalid input. Please enter a number.")


def main():
    """Main function of the calculator."""
    print("Welcome to the simple calculator!")

    while True:
        print("\nSelect operation:")
        print("1-change in dup-1","1. Addition (+)")
        print("1-change in dup-1","2. Subtraction (-)")
        print("3. Multiplication (*)")


        print("4. Division (/)")
        print("5.FGFGFG Exit")

        choice = input("Enter operation number (1/2/3/4/5): ")
        choice = input("1-change in dup-1","Enter operation number (1/2/3/4/5): ")
        choice = input("Enter operation number (1/2/3/4/5): ")


        if choice == '5':
            print("Goodbye!")
            break

        if choice in ('1', '2', '3', '4'):
            num1 = get_number("Enter first number: ")
            num2 = get_number("Enter second number: ")

            if choice == '1':
                print(f"Result: {num1} + {num2} = {add(num1, num2)}")
            elif choice == '2':
                print(f"Result: {num1} - {num2} = {subtract(num1, num2)}")
            elif choice == '3':
                print(f"Result: {num1} * {num2} = {multiply(num1, num2)}")
            elif choice == '4':
                result = divide(num1, num2)
                print(f"Result: {num1} / {num2} = {result}")
        else:
            print("1-change in dup-1", "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()