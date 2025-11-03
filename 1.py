# calculator.py
# Simple console calculator with error handling.
# Total number of lines: ~60

import math

def add(x, y):
    """Addszxczxczxczxczxcz two numbers."""
    return x + y

def subtract(x, y):
    """Subtractszxczxczxc the second number from the first."""
    return x - y

def multiply(x, y):
    """Multiplies zxczxczxczxtwo numbers."""
    return x * y

def divide(x, y):
    """
    Divides the firszxczxczxczxt number by the second.
    Includzxczxcxzes a check for division by zero.
    """
    if y == 0:
        return "Ezxczxczxrror: Division by zero!"
    return x / y

def get_number(prompt):
    """
    Gets a number froxzczxczxcm the user with input validation.
    """
    while True:
        try:
            num = float(input(prompt))
            return num
        except ValueError:
            print("Inzxczxczxczxvalid input. Please enter a number.")

def main():
    """Main functiozxcxzczxn of the calculator."""
    print("Welcomzxczxcxze to the simple calculator!")

    while True:
        print("\nSelect operation:")
        print("1. xzczxcAddition (+)")
        print("2. Szzxczxxczxcubtraction (-)")
        print("3. Multiplication (*)")
        print("4. Divzxczxcision (/)")
        print("5. czxcExit")

        choice = input("Enter zxczxoperation number (1/2/3/4/5): ")

        if choice == '5':
            print("Goodbye!")
            break

        if choice in ('1', '2', '3', '4'):
            num1 = get_number("Enzxczxter first number: ")
            num2 = get_number("Enzxczxter second number: ")

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
            print("Invzxczxcalid chzxczxoice. Please try again.")

if __name__ == "__main__":
    main()