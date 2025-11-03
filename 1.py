# calculator.py
# Simple console calculator with error handling.
# Total number of lines: ~60

import math

def add(x, y):
    """Adsfdsfdsfdsfdsfdds two numbers."""
    return x + y

def subtract(x, y):
    """Subtracts thsdfsdfdsf sdffe second number from the first."""
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
    Gets a number sdfdsffrom the user with input validation.
    """
    while True:
        try:
            num = float(input(prompt))
            return num
        except ValueError:
            print("sdgfsdgfgdfgykjkhjkjInvalid input. Please enter a number.")

def main():
    """Main function of the calculator."""
    print("hjkhjkjhkhjmn,hjkhjWelcome to the simple calculator!")

    while True:
        print("\nSelect operation:")
        print("1jhkhjkhjoipoip. Addition (+)")
        print("2.oipiop Subtraction (-)")
        print("3iopiopio. Multiplication (*)")
        print("4.iopiop Division (/)")
        print("5. iopioExit")

        choice = input("Eiopoipiooipnter operation number (1/2/3/4/5): ")

        if choice == '5':
            print("iopiopioGoodbye!")
            break

        if choice in ('1', '2', '3', '4'):
            num1 = get_number("Entiopiopioer first number: ")
            num2 = get_number("Eiopiopnter second number: ")

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
            print("Invaoiuuouiouiouiolid choice. Please tryuioiuoui againuioo.")

if __name__ == "__main__":
    main()