import os
import threading
import time
from datetime import datetime

users = {}
expenses = {}
lock = threading.Lock()

def log_action(username, action, error= None):
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    log_entry = f"[{'ERROR' if error else 'INFO'}] [{timestamp}] [{username}] – {action}"
    if error:
        log_entry += f", Error: {error}"
    with open("app.log", "a") as log_file:
        log_file.write(log_entry + "\n")

def save_data():
    while True:
        time.sleep(10)

        with lock:
            with open("users.txt", "w") as user_file:
                for username, password in users.items():
                    user_file.write(f"{username}:{password}\n")
            with open("ecpenses.txt", "w") as expense_file:
                for username, user_expenses in expenses.items():
                    for category, amount in user_expenses:
                        expense_file.write(f"{username}:{category}:{amount}\n")
        log_action("Программа", "Все сохранено в файл")

def register():
    username = input("Введите логин: ")
    if username in users:
        print("Пользователь с таким логином уже существует.")
        log_action(username, "Попытка регестрации под существующим пользователем", "Пользователь уже существует")
        return
    password = input("Введите пароль: ")
    users[username] = password
    expenses[username] = []
    print("Регистрация прошла успешно")
    log_action(username, "Успешная регестрация")

def login():
    username = input("Введите логин: ")
    password = input("Введите пароль: ")
    if username in users and users[username] == password:
        print("Авторизация прошла успешно.")
        log_action(username, "Успешная авторизация")
        return username
    else:
        print("Неверный логин или пароль.")
        log_action(username, "Неудачная попытка входа", "Неправильное имя или пароль")
        return None
    
def add_expense(username):
    category = input("Введите категорию расхода: ")
    try:
        amount = float(input("Введите сумму расхода: "))
        with lock:
            expenses[username].append((category, amount))
        print("Расход добавлен.")
        log_action(username, f"Расход добавлен : {category} - {amount}")
    except ValueError:
        print("Неверный формат суммы.")
        log_action(username, "Неудачная попытка добавления категории ", "Неверный формат суммы")

def view_expenses(username):
    if username in expenses and expenses[username]:
        print("Ваши расходы:")
        for category, amount in expenses[username]:
            print(f"{category}: {amount}")
        log_action(username, "Просмотр расхода")
    else:
        print("У вас нет расходов.")
        log_action(username, "Попытка посмотреть расход", "Расход не найден")

def main():
    save_thread = threading.Thread(target=save_data, daemon=True)
    save_thread.start()

    while True:
        print("\n1. Регистрация")
        print("2. Авторизация")
        print("3. Выход")
        choice = input("Выберите действие: ")

        if choice == "1":
            register()
        elif choice == "2":
            username = login()
            if username:
                while True:
                    print("\n1. Добавить расход")
                    print("2. Просмотреть расходы")
                    print("3. Выйти из аккаунта")
                    user_choice = input("Выберите действие: ")

                    if user_choice == "1":
                        add_expense(username)
                    elif user_choice == "2":
                        view_expenses(username)
                    elif user_choice == "3":
                        log_action(username, "Выход из аккаунта")
                        break
                    else:
                        print("Неверный выбор.")
        elif choice == "3":
            print("Выход из программы.")
            log_action("Программа", "Программа завершена")
            break
        else:
            print("Неверный выбор.")

if __name__ == "__main__":
    main()