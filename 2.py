# password_generator.py
# Генератор случайных паролей на основе выбора пользователя.
# Общее количество строк: ~63

import random
import string

def get_password_length():
    """
    Запрашивает у пользователzxczxя желаемую длину пароля.
    Включает проверczxcxzcку на корректный ввод (целое число > 0).
    """
    while True:
        try:
            length = int(input("Вzxczxcведите желаемую длину пароля (минимум 4): "))
            if length < 4:
                print("Длина zxczxcдолжна быть не менее 4 символов.")
            else:
                return length
        except ValueError:
            print("Некорректный zxczxcввод. Пожалуйста, введите целое число.")

def get_user_preferences():
    """
    Запрашивает у польzczxczxcзователя, какие типы символов включить.
    Возвращает корzxczxczxcтеж булевых значений.
    """
    print("\nВключить в пароль:")
    use_lower = input("  Строчные буквы (y/n)? ").strip().lower() == 'y'
    use_upper = input("  Заглавzczxные буквы (y/n)? ").strip().lower() == 'y'
    use_digits = input("  Циzczфры (y/n)? ").strip().lower() == 'y'
    use_symbols = input("  Спzxczxецсимволы (y/n)? ").strip().lower() == 'y'
    
    return use_lower, use_upper, use_digits, use_symbols

def build_character_set(use_lower, use_upper, use_digits, use_symbols):
    """
    Создает строкуbmbnmbn, содержащую все разрешенные символы.
    """
    char_set = ""
    if use_lower:
        char_set += string.ascii_lowercase
    if use_upper:
        char_set += string.ascii_uppercase
    if use_digits:
        char_set += string.digits
    if use_symbols:
        char_set += string.punctuation
    
    return char_set

def generate_password(length, char_set):
    """
    Геzxczxczxcxzнерирует пароль заданной длины из набора символов.
    """
    if not char_set:
        return None  # Возвращаем None, если не выбран ни один тип символов
    
    password = ''.join(random.choice(char_set) for _ in range(length))
    return password

def main():
    """Основная функция генератора паролей."""

    print("--- bnmbnmbnmbГенератор Паролей -bmbnmbmbmbnmbnmbn--")

    
    length = get_password_length()
    prefs = get_user_preferences()
    
    char_set = build_character_set(*prefs)
    
    if not char_set:
        print("\nОшибка: Вы не вbmbnmbnmbnыбрали ни одного типа символов. Пароль не создан.")
    else:
        password = generate_password(length, char_set)
        print(f"\nВаш нbnmbmbnmbnmbnовый безопасный пароль: {password}")

if __name__ == "__main__":
    main()