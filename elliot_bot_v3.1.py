import json
import os
import hashlib


def hash_password(password):
    """
    Простое хэширование для учебного проекта.
    В реальном проекте используй:
    import secrets
    salt = secrets.token_hex(16)
    return hashlib.sha256((password + salt).encode()).hexdigest()
    """
    return hashlib.sha256(password.encode()).hexdigest()

HOME_DIR = os.path.expanduser("~")
USERS_FILE = os.path.join(HOME_DIR, "elliot_users.json")

# Проверяем, существует ли файл с паролями
if os.path.exists(USERS_FILE):
    print("Используется локальная база данных")
else:
    print("База данных не найдена. Создаем новую...")
    # Создаем пустую базу
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump({}, f)

# Класс Ошибок для бота
class ElliotBotError(Exception):
    def __init__(self, message="Возникла ошибка"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"[ElliotBot Error] {self.message}"


class InvalidCommandError(ElliotBotError):
    def __init__(self, command):
        super().__init__(f"Неизвестная команда боту команда: '{command}'")


class NotFoundFunctionError(ElliotBotError):
    def __init__(self, function_num):
        super().__init__(f"Функция {function_num} не найдена")


class ValidationError(ElliotBotError):
    def __init__(self, value, expected):
        super().__init__(f"Написано некорректно: '{value}'. Ожидалось : {expected}")


class MathError(ElliotBotError):
    def __init__(self, operation, details=""):
        message = f"Возникла ошибка в математической операции '{operation}'"
        if details:
            message += f": {details}"
        super().__init__(message)

def save_user(user_id, login, password, is_admin=False):
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
    except FileNotFoundError:
        users = {}
    
    # Хэшируем пароль перед сохранением
    hashed_password = hash_password(password)
    
    users[user_id] = {
        "login": login,
        "password": hashed_password,
        "commands": {},
        "admin": is_admin
    }
    
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2, ensure_ascii=False)
    
    print(f"Пользователь {login} сохранён с ID: {user_id}")

def get_new_user_name_id():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
        return str(len(users) + 1)
    except FileNotFoundError:
        return "1"

def login_user():
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            users = json.load(f)
    except FileNotFoundError:
        print("В базе данных не найдено. Сначала зарегистрируйтесь.")
        return None
    
    print(" ВХОД В СИСТЕМУ ")
    
    for попытка in range(3):
        print(f"Попытка {попытка + 1} из 3")
        login = input("Логин: ")
        password = input("Пароль: ")
        
        # Хэшируем введенный пароль для сравнения
        hashed_password = hash_password(password)
        
        for user_id, user_data in users.items():
            if user_data["login"] == login and user_data["password"] == hashed_password:
                print(f"Успешный вход! Привет, {login}!")
                if user_data.get("admin"):
                    print("Вы вошли как Администратор Бота")
                return {
                    "id": user_id,
                    "login": login,
                    "is_admin": user_data.get("admin", False)
                }
        
        print("Неверный логин или пароль!")
    
    print("Слишком много неудачных попыток.")
    return None


# Основной код
print("Привет, я Бот Эллиот")

while True:
    print("ВХОД / РЕГИСТРАЦИЯ")
    print("1 - Вход в аккаунт")
    print("2 - Регистрация")
    print("3 - Выход")
    
    try:
        выбор = input("Выберите (1-3): ").strip()
        
        if выбор not in ["1", "2", "3"]:
            raise NotFoundFunctionError(выбор)
        
        if выбор == "1":
            user_data = login_user()
            if user_data:
                user_name = user_data["login"]
                user_name_id = user_data["id"]
                is_admin = user_data["is_admin"]
                break
            else:
                print("Вход не удался. Попробуйте снова или зарегистрируйтесь.")
        
        elif выбор == "2":
            print("РЕГИСТРАЦИЯ")
            print("Создайте имя пользователю:")
            user_name = input('>')
            print("Теперь пароль пользователю:")
            password_user_name = input('>')
            
            user_name_id = get_new_user_name_id()
            save_user(user_name_id, user_name, password_user_name)
            
            print(f"Вы зарегистрировались, теперь {user_name} вы есть в Бот Эллиоте")
            print(f"Ваш уникальный айди: {user_name_id}")
            
            user_data = {
                "id": user_name_id,
                "login": user_name,
                "is_admin": False
            }
            is_admin = False
            break
        
        elif выбор == "3":
            print("До свидания!")
            exit()
    
    except NotFoundFunctionError as elliot_bot_registr:
        print(f"Ошибка: {elliot_bot_registr}")
        print("Пожалуйста, выберите 1, 2 или 3")



функции_бота = {
    "1": {
        "название": "Математика",
        "описание": "Ответы на математические вопросы"
    },
    "2": {
        "название": "Python помощь",
        "описание": "Помощь с кодом(Python)"
    },
    "3": {
        "название": "Фишки ПК",
        "описание": "Фишки для компьютера/ноутбука"
    },
    "4": {
        "название": "Командная строка",
        "описание": "Фишки с командной строкой"
    },
    "5": {
        "название": "Установка ОС",
        "описание": "Установка Windows/Linux"
    }
    
}

while True:
    try:
        рассказать_о_функциях = input("Рассказать о моих функциях (да/нет): ").strip().lower()
        
        if рассказать_о_функциях not in ['да', 'нет']:
            raise ValidationError(рассказать_о_функциях, "'да' или 'нет'")
        
        break
        
    except ValidationError as elliot_bot_error_1:
        print(f" {elliot_bot_error_1}")
        print("Пожалуйста, введите 'да' или 'нет'")

if рассказать_о_функциях == "нет":
    print("Тогда ладно")
    print("Но знай: я могу рассказать о функциях")
    print("/help - помощь с командами")

elif рассказать_о_функциях == "да":
    print("Сейчас же расскажу!")
    print("Вот мои функции:")
    for номер, данные in функции_бота.items():
        print(f"{номер}- {данные['описание']}")

while True:
    try:
        выбрать_функцию = input("Выбрать функцию 1-5: ")

        if выбрать_функцию == "1":
            print("Математика")

            def получить_число(запрос):
                while True:
                    try:
                        ввести_число = input(запрос).strip()
                        if '.' in ввести_число:
                            return float(ввести_число)
                        else:
                            return int(ввести_число)
                    except:
                        print("Надо ввести число! Попробуйте снова:")

            while True:
                print("Выберите операцию:")
                print("1- Сложение")
                print("2- Вычитание")
                print("3- Умножение")
                print("4- Деление")
                print("5- Ничего: выход из функции")

                try:
                    математическая_операция = input("Выбирай: (1-5):").strip()

                    if математическая_операция == "5":
                        print("Выхожу из данной функции")
                        break

                    if математическая_операция not in ["1", "2", "3", "4"]:
                        raise NotFoundFunctionError(математическая_операция)

                    число_1 = получить_число("Это первое число: ")
                    число_2 = получить_число("Это второе число: ")

                    if математическая_операция == "1":
                        результат = число_1 + число_2
                        знак = "+"
                    elif математическая_операция == "2":
                        результат = число_1 - число_2
                        знак = "-"
                    elif математическая_операция == "3":
                        результат = число_1 * число_2
                        знак = "*"
                    elif математическая_операция == "4":
                        if число_2 == 0:
                            raise MathError("Делить на ноль нельзя!")
                        результат = число_1 / число_2
                        знак = "÷"

                    print(f"Результат: {число_1} {знак} {число_2} = {результат}")

                    while True:
                        ещё_раз_посчитать = input("Хотите ещё раз посчитаю? (да/нет): ").strip().lower()
                        if ещё_раз_посчитать in ["да", "нет"]:
                            break
                        print("Напиши 'да' или 'нет'")

                    if ещё_раз_посчитать == "нет":
                        print("Заканчиваю данную функцию")
                        break

                except NotFoundFunctionError as elliot_bot_error_1:
                    print(f"Ошибка: {elliot_bot_error_1}")
                except MathError as elliot_bot_error_1:
                    print(f" {elliot_bot_error_1}")
                except Exception as elliot_bot_error_1:
                    print(f"Что-то пошло не так: {elliot_bot_error_1}")

        elif выбрать_функцию == "2":
            print("Помощь с кодом(Python)")

            while True:
                print("Выбирай:")
                print("1- Основы Python")
                print("2- Примеры кода")
                print("3- Ошибки новичков")
                print("4- Советы")
                print("5- Ничего:выход из функции")

                try:
                    выбор_py = input("Твой выбор (1-5):").strip()

                    if выбор_py == "5":
                        print("Выхожу из функции")
                        break

                    if выбор_py not in ["1", "2", "3", "4"]:
                        raise NotFoundFunctionError(выбор_py)

                    if выбор_py == "1":
                        print(" Основы Python ")
                        print("Переменные:")
                        print("x = 10")
                        print('имя = "Алекс"')
                        print("список = [1, 2, 3]")
                        print("Условия:")
                        print("if возраст >= 18:")
                        print("    print('Взрослый')")
                        print("else:")
                        print("    print('Ребёнок')")
                        print("Циклы:")
                        print("for i in range(3):")
                        print("    print(i)")
                        print("Функции:")
                        print("def приветствие(имя):")
                        print('    print(f"Привет, {имя}!")')
                        print('приветствие("Алекс")')

                    elif выбор_py == "2":
                        print(" Примеры кода ")
                        print("Работа со списком:")
                        print("числа = [5, 2, 8, 1]")
                        print('print(f"Список: {числа}")')
                        print('print(f"Сумма: {sum(числа)}")')
                        print('print(f"Отсортированный: {sorted(числа)}")')
                        print("Чтение файла:")
                        print("with open('test.txt', 'w') as f:")
                        print('    f.write("Привет, мир!")')
                        print("with open('test.txt', 'r') as f:")
                        print("    содержимое = f.read()")
                        print("    print(содержимое)")

                    elif выбор_py == "3":
                        print(" Ошибки новичков ")
                        print("1. Забыл двоеточие:")
                        print("   if x > 5  # ОШИБКА")
                        print("   if x > 5:  # ПРАВИЛЬНО")
                        print("2. Неправильные отступы:")
                        print("   if x > 5:")
                        print("   print('Привет')  # ОШИБКА")
                        print("   if x > 5:")
                        print("       print('Привет')  # ПРАВИЛЬНО")
                        print("3. Деление на ноль:")
                        print("   print(10 / 0)  # ОШИБКА")
                        print("   if b != 0:")
                        print("       print(a / b)  # ПРАВИЛЬНО")

                    elif выбор_py == "4":
                        print(" Советы ")
                        print("1. Комментируй код:")
                        print("   # Это помогает понять код")
                        print("   x = 5  # количество попыток")
                        print("2. Используй понятные имена:")
                        print("   плохо: a = 10")
                        print("   хорошо: возраст = 10")
                        print("3. Проверяй по частям:")
                        print("   Не пиши всю программу сразу")
                        print("   Проверяй каждую часть отдельно")
                        print("4. Читай ошибки:")
                        print("   Python сам говорит где ошибка")

                    input("Нажмите Enter чтобы продолжить...")

                except NotFoundFunctionError as elliot_bot_error_2:
                    print(f"Ошибка: {elliot_bot_error_2}")
                    print("Выбери 1, 2, 3 или 4")

                while True:
                    ещё = input("Ещё про Python? (да/нет): ").strip().lower()
                    if ещё in ["да", "нет"]:
                        break
                    print("Напиши 'да' или 'нет'")

                if ещё == "нет":
                    print("Выхожу из помощи по Python...")
                    break

        elif выбрать_функцию == "3":
            print("Фишки для ПК/Ноутбука")

            while True:
                print("Что вы выберите?")
                print("1- Ускорение Windows")
                print("2- Горячие клавиши")
                print("3- Очистка системы")
                print("4- Безопасность пользователя")
                print("5- Ничего: выход из функции")

                try:
                    выбор_фишек = input("Выберите: 1-5:")

                    if выбор_фишек == "5":
                        print("Выхожу из данной функции")
                        break

                    if выбор_фишек not in ["1", "2", "3", "4"]:
                        raise NotFoundFunctionError(выбор_фишек)
                    
                    if выбор_фишек == "1":
                        print(" Ускорение Windows ")
                        print("1. Отключи ненужные службы:")
                        print("   Win+R → services.msc")
                        print("   Отключи:")
                        print("   - Windows Search")
                        print("   - Xbox Live Auth Manager")
                        print("   - Printer Spooler (если нет принтера)")
                        
                        print("2. Автозагрузка:")
                        print("   Ctrl+Shift+Esc → Автозагрузка")
                        print("   Отключи ненужные программы")
                        
                        print("3. Визуальные эффекты:")
                        print("   Win+Pause → Доп. параметры")
                        print("   Быстродействие → Параметры")
                        print("   Выбери 'Обеспечить лучший быстродействие'")
                    
                    elif выбор_фишек == "2":
                        print(" Горячие клавиши ")
                        print("Win + D - Рабочий стол")
                        print("Win + E - Проводник")
                        print("Win + L - Заблокировать ПК")
                        print("Win + Shift + S - Скриншот области")
                        print("Ctrl + Shift + Esc - Диспетчер задач")
                        print("Alt + Tab - Переключение окон")
                        print("Win + Tab - Предпросмотр окон")
                        print("Ctrl + C / V - Копировать/Вставить")
                        print("Ctrl + Z - Отменить")
                        print("Ctrl + Shift + N - Новая папка")
                    
                    elif выбор_фишек == "3":
                        print(" Очистка системы ")
                        print("1. Очистка диска:")
                        print("   Win+R → cleanmgr → Enter")
                        print("   Выбери диск C:")
                        print("   Отметь все галочки → ОК")
                        
                        print("2. Удаление временных файлов:")
                        print("   Win+R → %temp% → Enter")
                        print("   Ctrl+A → Delete")
                        
                        print("3. Очистка кэша:")
                        print("   Браузер Chrome:")
                        print("   Ctrl+Shift+Delete → Выбери 'Все время'")
                        print("   Отметь: Кэш, Куки → Удалить")
                        
                        print("4. CCleaner (программа):")
                        print("   Бесплатная версия")
                        print("   Сканировать → Очистить")
                    
                    elif выбор_фишек == "4":
                        print(" Безопасность ")
                        print("1. Антивирус:")
                        print("   Windows Defender (встроенный)")
                        print("   Или: Kaspersky Free, Avast Free")
                        
                        print("2. Брандмауэр:")
                        print("   Панель управления → Брандмауэр")
                        print("   Включи входящие/исходящие правила")
                        
                        print("3. Обновления:")
                        print("   Win+I → Обновление и безопасность")
                        print("   Проверь наличие обновлений")
                        
                        print("4. Резервное копирование:")
                        print("   Win+I → Обновление → Резервное копирование")
                        print("   Добавь диск → Включи")
                        
                        print("5. Пароли:")
                        print("   Используй менеджер паролей:")
                        print("   - Bitwarden (бесплатный)")
                        print("   - LastPass (бесплатный)")
                        print("   Не используй один пароль везде!")
                    
                    input("Нажми Enter чтобы продолжить...")
                    
                except NotFoundFunctionError as elliot_bot_error_3:
                    print(f"Ошибка: {elliot_bot_error_3}")
                    print("Выбери 1, 2, 3 или 4")
                
                while True:
                    ещё = input("Ещё советы по компьютеру? (да/нет): ").strip().lower()
                    if ещё in ["да", "нет"]:
                        break
                    print("Напиши 'да' или 'нет'")
                
                if ещё == "нет":
                    print("Заканчиваю компьютерные советы...")
                    break

        elif выбрать_функцию == "4":
            print("Фишки с командной строкой")

            while True:
                print("Что интересует?")
                print("1- Windows CMD")
                print("2- PowerShell")
                print("3- Linux/Mac Terminal")
                print("4- Полезные команды")
                print("5- Ничего: выход из функции")
                
                try:
                    выбор_фишек__с_командной_строкой = input("Твой выбор (1-5): ").strip()
                    
                    if выбор_фишек__с_командной_строкой == "5":
                        print("Выхожу из командной строки...")
                        break
                    
                    if выбор_фишек__с_командной_строкой not in ["1", "2", "3", "4"]:
                        raise NotFoundFunctionError(выбор_фишек__с_командной_строкой)
                    
                    if выбор_фишек__с_командной_строкой == "1":
                        print(" WINDOWS CMD ")
                        print("Основные команды:")
                        print("dir           - список файлов в папке")
                        print("cd folder     - войти в папку")
                        print("cd ..         - выйти на уровень выше")
                        print("mkdir folder  - создать папку")
                        print("rmdir folder  - удалить папку")
                        print("del file.txt  - удалить файл")
                        print("copy a.txt b.txt - копировать файл")
                        print("move a.txt folder/ - переместить файл")
                        print("type file.txt - показать содержимое файла")
                        print("cls           - очистить экран")
                        print("help          - помощь по командам")
                        print("Сетевые команды:")
                        print("ipconfig      - информация о сети")
                        print("ping google.com - проверить соединение")
                        print("tracert google.com - путь до сайта")
                        print("netstat -an   - активные соединения")
                    
                    elif выбор_фишек__с_командной_строкой == "2":
                        print(" POWERSHELL ")
                        print("Основные команды:")
                        print("Get-ChildItem       - список файлов (как dir)")
                        print("Set-Location folder - войти в папку")
                        print("New-Item folder -Type Directory - создать папку")
                        print("Remove-Item file.txt - удалить файл")
                        print("Copy-Item src dst - копировать")
                        print("Move-Item src dst - переместить")
                        print("Get-Content file.txt - показать содержимое")
                        print("Clear-Host       - очистить экран")
                        print("Get-Help команда - помощь по команде")
                        print("Полезные фишки:")
                        print("Get-Process | Where CPU -gt 50")
                        print("  # процессы с нагрузкой CPU > 50%")
                        print("Get-Service | Select Name, Status")
                        print("  # список всех служб")
                        print("Get-EventLog -LogName System -Newest 10")
                        print("  # последние 10 событий из лога")
                    
                    elif выбор_фишек__с_командной_строкой == "3":
                        print(" LINUX/MAC TERMINAL ")
                        print("Основные команды:")
                        print("ls          - список файлов")
                        print("cd folder   - войти в папку")
                        print("cd ..       - выйти на уровень выше")
                        print("mkdir folder - создать папку")
                        print("rm file.txt - удалить файл")
                        print("rm -rf folder/ - удалить папку с файлами")
                        print("cp src dst  - копировать")
                        print("mv src dst  - переместить/переименовать")
                        print("cat file.txt - показать содержимое файла")
                        print("clear       - очистить экран")
                        print("man команда - справка по команде")
                        print("Полезные команды:")
                        print("sudo        - выполнить как администратор")
                        print("pwd         - текущая папка")
                        print("whoami      - текущий пользователь")
                        print("ps aux      - запущенные процессы")
                        print("top         - мониторинг системы")
                        print("grep текст файл - поиск текста в файле")
                        print("chmod +x script.sh - сделать файл исполняемым")
                    
                    elif выбор_фишек__с_командной_строкой == "4":
                        print(" ПОЛЕЗНЫЕ КОМАНДЫ ")
                        print("1. Проверка диска:")
                        print("   Windows: chkdsk C:")
                        print("   Linux: df -h")
                        print("2. Поиск файлов:")
                        print("   Windows: dir /s *.txt")
                        print("   Linux: find / -name \"*.txt\"")
                        print("3. Архивация:")
                        print("   Windows: tar -cvf archive.tar folder/")
                        print("   Linux: tar -xvf archive.tar")
                        print("4. Сеть:")
                        print("   nslookup google.com - DNS запрос")
                        print("   netstat -r         - таблица маршрутизации")
                        print("5. Система:")
                        print("   Windows: systeminfo")
                        print("   Linux: uname -a")
                        print("   Mac: sw_vers")
                        print("6. Бэкап важных файлов:")
                        print("   Windows: xcopy C:\\docs D:\\backup\\ /E /H /C /I")
                        print("   Linux: cp -r ~/docs /backup/")
                    
                    input("Нажми Enter чтобы продолжить...")
                    
                except NotFoundFunctionError as elliot_bot_error_4:
                    print(f"Ошибка: {elliot_bot_error_4}")
                    print("Выбери 1, 2, 3 или 4")
                
                while True:
                    ещё = input("Ещё про командную строку? (да/нет): ").strip().lower()
                    if ещё in ["да", "нет"]:
                        break
                    print("Напиши 'да' или 'нет'")
                
                if ещё == "нет":
                    print("Выхожу из командной строки...")
                    break

        elif выбрать_функцию == "5":
            print("Установка windows/linux")

            while True:
                print("Что нужно?")
                print("1- Установка Windows")
                print("2- Установка Linux")
                print("3- Создание загрузочной флешки")
                print("4- Драйверы и настройка")
                print("5- Ничего: выход из функции")
                
                try:
                    выбор_что_нужно_для_системы = input("Твой выбор (1-5): ").strip()
                    
                    if выбор_что_нужно_для_системы == "5":
                        print("Выхожу из установки ОС...")
                        break
                    
                    if выбор_что_нужно_для_системы not in ["1", "2", "3", "4"]:
                        raise NotFoundFunctionError(выбор_что_нужно_для_системы)
                    
                    if выбор_что_нужно_для_системы == "1":
                        print(" УСТАНОВКА WINDOWS ")
                        print("1. Скачай Media Creation Tool")
                        print("2. Создай загрузочную флешку")
                        print("3. Перезагрузи ПК, зайди в Boot Menu")
                        print("4. Выбери флешку")
                        print("5. Следуй инструкциям")
                        print("6. Форматируй диск, устанавливай")
                        print("7. Установи драйверы")
                        print("8. Обнови Windows")
                    
                    elif выбор_что_нужно_для_системы == "2":
                        print(" УСТАНОВКА LINUX UBUNTU ")
                        print("1. Скачай Ubuntu с ubuntu.com")
                        print("2. Используй Rufus для записи на флешку")
                        print("3. Перезагрузи, зайди в Boot Menu")
                        print("4. Выбери флешку")
                        print("5. Выбери 'Try Ubuntu' или 'Install'")
                        print("6. Следуй инструкциям")
                        print("7. После установки:")
                        print("   sudo apt update")
                        print("   sudo apt upgrade")
                        print("   sudo apt install software-properties-common")
                    
                    elif выбор_что_нужно_для_системы == "3":
                        print(" ЗАГРУЗОЧНАЯ ФЛЕШКА ")
                        print("1. Скачай образ ОС (.iso)")
                        print("2. Скачай Rufus (Windows) или balenaEtcher")
                        print("3. Подключи флешку 8+ GB")
                        print("4. В Rufus выбери флешку и образ")
                        print("5. Нажми Start (данные удалятся!)")
                        print("6. Жди 5-30 минут")
                        print("7. Готово!")
                    
                    elif выбор_что_нужно_для_системы == "4":
                        print(" ДРАЙВЕРЫ И НАСТРОЙКА ")
                        print("1. Видеокарта: сайт NVIDIA/AMD/Intel")
                        print("2. Материнская плата: сайт производителя")
                        print("3. Или используй DriverPack Solution")
                        print("4. Обязательные программы:")
                        print("   - Браузер (Chrome/Firefox)")
                        print("   - Антивирус")
                        print("   - Архиватор (7-Zip)")
                        print("   - Офис (Office/LibreOffice)")
                        print("   - Медиаплеер (VLC)")
                    
                    input("Нажми Enter чтобы продолжить...")
                    
                except NotFoundFunctionError as elliot_bot_error_5:
                    print(f"Ошибка: {elliot_bot_error_5}")
                    print("Выбери 1, 2, 3 или 4")
                
                while True:
                    ещё = input("Ещё про установку ОС? (да/нет): ").strip().lower()
                    if ещё in ["да", "нет"]:
                        break
                    print("Напиши 'да' или 'нет'")
                
                if ещё == "нет":
                    print("Выхожу из установки ОС...")
                    break

        else:
            raise NotFoundFunctionError(выбрать_функцию)

    except NotFoundFunctionError as elliot_bot_error_0:
        print(f"Ошибка произошла у бота: {elliot_bot_error_0}")
        print("Пожалуйста,выберите функцию 1-5")
        continue

    while True:
        try:
            выбрать_функцию_ещё_раз = input("Выбрать функцию ещё раз(да/нет): ").strip().lower()
            
            if выбрать_функцию_ещё_раз not in ['да', 'нет']:
                raise ValidationError(выбрать_функцию_ещё_раз, "'да' или 'нет'")
            
            break
            
        except ValidationError as elliot_bot_error_1:
            print(f" {elliot_bot_error_1}")
            print("Пожалуйста, введите 'да' или 'нет'")
    
    if выбрать_функцию_ещё_раз == "нет":
        print("Вы отказались от выбора функций.")
        break
