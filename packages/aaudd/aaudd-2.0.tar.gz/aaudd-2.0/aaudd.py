import os
import platform
import requests

TOKEN_FILE = "api_token.txt"
LANGUAGE_FILE = "language.txt"

def clear_console():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def get_api_token():
    if os.path.isfile(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as file:
            return file.read().strip()
    else:
        while True:
            language = get_language()
            if language == 'english':
                api_token = input("Enter your Audd.io API token: ")
            else:
                api_token = input("Введите ваш API-токен Audd.io: ")
            if api_token.strip():
                with open(TOKEN_FILE, 'w') as file:
                    file.write(api_token)
                return api_token
            else:
                if language == 'english':
                    print("Token cannot be empty. Please try again.")
                else:
                    print("Токен не может быть пустым. Попробуйте еще раз.")

def get_language():
    if os.path.isfile(LANGUAGE_FILE):
        with open(LANGUAGE_FILE, 'r') as file:
            return file.read().strip()
    else:
        while True:
            print("1. English")
            print("2. Русский")
            language_choice = input("Select language (1/2): ")
            if language_choice == '1':
                with open(LANGUAGE_FILE, 'w') as file:
                    file.write('english')
                return 'english'
            elif language_choice == '2':
                with open(LANGUAGE_FILE, 'w') as file:
                    file.write('русский')
                return 'русский'
            else:
                print("Invalid input. Please try again.")

def update_api_token():
    while True:
        language = get_language()
        if language == 'english':
            update_option = input("Do you want to update the API token? (Y/N): ").lower()
        else:
            update_option = input("Хотите ли вы обновить API-токен? (Y/N): ").lower()
        if update_option == 'y':
            if language == 'english':
                new_token = input("Enter a new Audd.io API token: ")
            else:
                new_token = input("Введите новый API-токен Audd.io: ")
            with open(TOKEN_FILE, 'w') as file:
                file.write(new_token)
            if language == 'english':
                print("API token updated successfully.")
            else:
                print("API-токен успешно обновлен.")
            return new_token
        elif update_option == 'n':
            return get_api_token()
        else:
            if language == 'english':
                print("Invalid input. Please try again.")
            else:
                print("Некорректный ввод. Попробуйте еще раз.")

def change_language():
    while True:
        language = get_language()
        if language == 'english':
            new_language_choice = input("Do you want to change the language to Русский? (Y/N): ").lower()
        else:
            new_language_choice = input("Хотите ли вы изменить язык на English? (Y/N): ").lower()
        if new_language_choice == 'y':
            if language == 'english':
                with open(LANGUAGE_FILE, 'w') as file:
                    file.write('русский')
            else:
                with open(LANGUAGE_FILE, 'w') as file:
                    file.write('english')
            if language == 'english':
                print("Language changed successfully.")
            else:
                print("Язык успешно изменен.")
            return
        elif new_language_choice == 'n':
            return
        else:
            if language == 'english':
                print("Invalid input. Please try again.")
            else:
                print("Некорректный ввод. Попробуйте еще раз.")

def main():
    clear_console()
    language = get_language()

    if language == 'english':
        print("Made by Avinion")
        print("Telegram: @akrim\n")
        print("1. Use current language")
        print("2. Change language")
        option = input("Enter your choice (1/2): ")
    else:
        print("Сделано Avinion")
        print("Telegram: @akrim\n")
        print("1. Использовать текущий язык")
        print("2. Изменить язык")
        option = input("Введите ваш выбор (1/2): ")

    if option == '2':
        change_language()
        return

    api_token = update_api_token()

    while True:
        if language == 'english':
            file_input = input("Enter the URL of the audio file or the local path to the file: ")
        else:
            file_input = input("Введите URL аудиофайла или локальный путь к файлу: ")

        is_url = False
        if file_input.startswith('http://') or file_input.startswith('https://'):
            is_url = True

        if is_url:
            url = file_input
            file_data = None
            file_name = None
        else:
            if os.path.isfile(file_input):
                with open(file_input, 'rb') as file:
                    file_data = file.read()
                file_name = os.path.basename(file_input)
                url = None
            else:
                if language == 'english':
                    print("The entered string is not a URL or a local file path.")
                else:
                    print("Введенная строка не является URL или локальным путем к файлу.")
                continue

        if language == 'english':
            services = input("Enter a list of services to return (separated by commas): ")
        else:
            services = input("Введите список сервисов для возврата (через запятую): ")

        data = {
            'api_token': api_token,
            'return': services
        }

        if url:
            data['url'] = url
            result = requests.post('https://api.audd.io/', data=data).json()
        else:
            files = {'file': (file_name, file_data)}
            result = requests.post('https://api.audd.io/', data=data, files=files).json()

        if 'result' in result:
            if language == 'english':
                output = "\nRecognition result:\n"
            else:
                output = "\nРезультат распознавания:\n"
            for key, value in result['result'].items():
                output += f"{key.capitalize()}: {value}\n"
        else:
            if language == 'english':
                output = "\nRecognition error:\n"
            else:
                output = "\nОшибка распознавания:\n"
            output += f"Error code: {result['error']['error_code']}\n"
            output += f"Error message: {result['error']['error_message']}\n"
            if 'warning' in result:
                output += f"Warning: {result['warning']['error_message']}\n"

        if language == 'english':
            save_option = input("Do you want to save the result in a text file? (y/n): ").lower()
        else:
            save_option = input("Хотите ли вы сохранить результат в текстовый файл? (y/n): ").lower()

        if save_option == 'y':
            if language == 'english':
                file_name = input("Enter a file name to save: ")
            else:
                file_name = input("Введите имя файла для сохранения: ")
            with open(f"{file_name}.txt", 'w') as file:
                file.write(output)
            if language == 'english':
                print(f"Result saved to {file_name}.txt")
            else:
                print(f"Результат сохранен в файле {file_name}.txt")
        else:
            print(output)

        if language == 'english':
            continue_option = input("Do you want to continue? (Y/N): ").lower()
        else:
            continue_option = input("Хотите продолжить работу? (Y/N): ").lower()

        if continue_option != 'y':
            break

if __name__ == "__main__":
    main()