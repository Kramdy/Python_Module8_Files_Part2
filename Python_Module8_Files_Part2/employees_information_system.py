import os

# Модуль 8. Файли. Частина 2
# Завдання
# Напишіть інформаційну систему «Співробітники». Програма має забезпечувати
# введення, редагування та видалення даних про співробітника, пошук за прізвищем,
# виведення співробітників вказаного віку або з прізвищем на вказану літеру.
# Зробіть збереження знайденої інформації та всього списку у файл. Під час старту
# завантажуйте список співробітників із зазначеного користувачем файлу.

DEFAULT_FILE = os.path.join(os.path.dirname(__file__), "employees.txt")


def load_employees(file_name):
    """Завантажує список співробітників з текстового файлу."""
    employees = []

    try:
        with open(file_name, "r", encoding="utf-8") as file:
            for line in file:
                data = line.strip().split("|")
                if len(data) == 5 and data[2].isdigit():
                    employees.append({
                        "surname": data[0],
                        "name": data[1],
                        "age": int(data[2]),
                        "position": data[3],
                        "phone": data[4],
                    })
    except FileNotFoundError:
        print("Файл не знайдено. Буде створено новий список.")
    except OSError:
        print("Не вдалося прочитати файл.")

    return employees


def save_employees(file_name, employees):
    """Зберігає список співробітників у текстовий файл."""
    try:
        with open(file_name, "w", encoding="utf-8") as file:
            for employee in employees:
                file.write(
                    f"{employee['surname']}|{employee['name']}|{employee['age']}|"
                    f"{employee['position']}|{employee['phone']}\n"
                )
        print("Інформацію збережено у файл:", file_name)
    except OSError:
        print("Не вдалося зберегти файл.")


def show_employees(employees):
    if not employees:
        print("Список порожній.")
        return

    for number, employee in enumerate(employees, start=1):
        print(
            f"{number}. {employee['surname']} {employee['name']}, "
            f"{employee['age']} років, {employee['position']}, {employee['phone']}"
        )


def input_age():
    while True:
        age_text = input("Вік: ").strip()
        if age_text.isdigit() and int(age_text) > 0:
            return int(age_text)
        print("Введіть додатне ціле число.")


def create_employee():
    return {
        "surname": input("Прізвище: ").strip(),
        "name": input("Ім'я: ").strip(),
        "age": input_age(),
        "position": input("Посада: ").strip(),
        "phone": input("Телефон: ").strip(),
    }


def add_employee(employees):
    employees.append(create_employee())
    print("Співробітника додано.")


def find_employee_index(employees):
    surname = input("Введіть прізвище: ").strip().lower()
    found_indexes = [
        index for index, employee in enumerate(employees)
        if employee["surname"].lower() == surname
    ]

    if not found_indexes:
        print("Співробітника не знайдено.")
        return None

    for index in found_indexes:
        employee = employees[index]
        print(f"{index + 1}. {employee['surname']} {employee['name']}")

    while True:
        number = input("Введіть номер співробітника: ").strip()
        if number.isdigit() and int(number) - 1 in found_indexes:
            return int(number) - 1
        print("Невірний номер.")


def edit_employee(employees):
    index = find_employee_index(employees)
    if index is None:
        return

    print("Введіть нові дані співробітника.")
    employees[index] = create_employee()
    print("Дані змінено.")


def delete_employee(employees):
    index = find_employee_index(employees)
    if index is None:
        return

    deleted_employee = employees.pop(index)
    print("Видалено:", deleted_employee["surname"], deleted_employee["name"])


def search_by_surname(employees):
    surname = input("Прізвище для пошуку: ").strip().lower()
    found = [
        employee for employee in employees
        if employee["surname"].lower() == surname
    ]
    show_employees(found)
    return found


def search_by_age(employees):
    age = input_age()
    found = [employee for employee in employees if employee["age"] == age]
    show_employees(found)
    return found


def search_by_letter(employees):
    letter = input("Перша літера прізвища: ").strip().lower()
    if not letter:
        print("Літеру не введено.")
        return []

    found = [
        employee for employee in employees
        if employee["surname"].lower().startswith(letter)
    ]
    show_employees(found)
    return found


def save_found_information(employees):
    if not employees:
        print("Немає знайденої інформації для збереження.")
        return

    file_name = input("Ім'я файлу для результату: ").strip()
    if file_name:
        save_employees(file_name, employees)


def main():
    print("Інформаційна система «Співробітники»")
    file_name = input("Шлях до файлу (Enter — employees.txt): ").strip()
    if not file_name:
        file_name = DEFAULT_FILE

    employees = load_employees(file_name)
    last_found = []

    while True:
        print("\n1 - додати співробітника")
        print("2 - редагувати співробітника")
        print("3 - видалити співробітника")
        print("4 - пошук за прізвищем")
        print("5 - пошук за віком")
        print("6 - пошук за першою літерою прізвища")
        print("7 - показати всіх")
        print("8 - зберегти знайдену інформацію")
        print("9 - зберегти весь список")
        print("0 - вихід")

        choice = input("Оберіть дію: ").strip()

        if choice == "1":
            add_employee(employees)
        elif choice == "2":
            edit_employee(employees)
        elif choice == "3":
            delete_employee(employees)
        elif choice == "4":
            last_found = search_by_surname(employees)
        elif choice == "5":
            last_found = search_by_age(employees)
        elif choice == "6":
            last_found = search_by_letter(employees)
        elif choice == "7":
            show_employees(employees)
        elif choice == "8":
            save_found_information(last_found)
        elif choice == "9":
            save_employees(file_name, employees)
        elif choice == "0":
            save_employees(file_name, employees)
            print("Програму завершено.")
            break
        else:
            print("Невірний вибір.")


if __name__ == "__main__":
    main()
