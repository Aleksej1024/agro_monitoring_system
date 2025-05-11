import requests
import random
from time import sleep
from threading import Thread
from faker import Faker

# Настройки
BASE_URL = "http://0.0.0.0:8000"  # Замените на ваш URL API
ADMIN_CREDENTIALS = {
    "username": "admin",
    "password": "password123"
}
NUM_USERS = 30  # Количество тестовых пользователей
NUM_FIELDS = 20  # Количество тестовых полей
NUM_TASKS = 50   # Количество тестовых задач
NUM_SEASONS = 15 # Количество тестовых сезонов

fake = Faker()

def get_auth_token():
    """Получение токена авторизации"""
    response = requests.post(
        f"{BASE_URL}/token",
        data=ADMIN_CREDENTIALS,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    return response.json()["access_token"]

def create_user(token, user_data):
    """Создание пользователя"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{BASE_URL}/users/",
        json=user_data,
        headers=headers
    )
    return response.json()

def create_field(token, field_data):
    """Создание поля"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{BASE_URL}/fields/",
        json=field_data,
        headers=headers
    )
    return response.json()

def create_task(token, task_data):
    """Создание задачи"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{BASE_URL}/tasks/",
        json=task_data,
        headers=headers
    )
    return response.json()

def create_season(token, season_data):
    """Создание сезона"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    response = requests.post(
        f"{BASE_URL}/seasons/",
        json=season_data,
        headers=headers
    )
    return response.json()

def populate_database():
    """Заполнение базы данных тестовыми данными"""
    print("Начинаем заполнение базы данных...")
    
    # Получаем токен админа
    token = get_auth_token()
    
    # Создаем тестовых пользователей
    users = []
    print(f"Создаем {NUM_USERS} тестовых пользователей...")
    for i in range(NUM_USERS):
        user_data = {
            "login": f"user{i+1}",
            "fio": fake.name(),
            "role": random.randint(1, 3),  # Случайная роль
            "password": "testpassword123"
        }
        user = create_user(token, user_data)
        users.append(user)
        print(f"Создан пользователь {user['login']}")
    
    # Создаем тестовые поля
    fields = []
    print(f"\nСоздаем {NUM_FIELDS} тестовых полей...")
    for i in range(NUM_FIELDS):
        field_data = {
            "location": fake.city() + " Field",
            "area": random.randint(10, 500),
            "status": random.randint(0, 2)
        }
        field = create_field(token, field_data)
        fields.append(field)
        print(f"Создано поле в {field_data['location']} площадью {field_data['area']} га")
    
    # Создаем тестовые задачи
    print(f"\nСоздаем {NUM_TASKS} тестовых задач...")
    for i in range(NUM_TASKS):
        task_data = {
            "description": fake.sentence(),
            "user_id": random.choice(users)["id"],
            "field_id": random.choice(fields)["id"]
        }
        task = create_task(token, task_data)
        print(f"Создана задача: {task_data['description']}")
    
    # Создаем тестовые сезоны
    print(f"\nСоздаем {NUM_SEASONS} тестовых сезонов...")
    for i in range(NUM_SEASONS):
        start_date = fake.date_between(start_date='-1y', end_date='today')
        end_date = fake.date_between(start_date=start_date, end_date='+1y')
        
        season_data = {
            "year": random.randint(2020, 2023),
            "culture": random.choice(["Wheat", "Corn", "Soybeans", "Barley", "Sunflower"]),
            "field_id": random.choice(fields)["id"],
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "start_volume": random.randint(100, 1000),
            "end_volume": random.randint(1000, 5000)
        }
        season = create_season(token, season_data)
        print(f"Создан сезон {season_data['culture']} с {season_data['start_date']} по {season_data['end_date']}")
    
    print("\nБаза данных успешно заполнена тестовыми данными!")

def load_test_user(user_id, token):
    """Функция для имитации работы одного пользователя"""
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        # 1. Получаем информацию о себе
        requests.get(f"{BASE_URL}/users/me/", headers=headers)
        
        # 2. Получаем список полей (с вероятностью 80%)
        if random.random() < 0.8:
            requests.get(f"{BASE_URL}/fields/", headers=headers)
        
        # 3. Получаем список задач (с вероятностью 60%)
        if random.random() < 0.6:
            requests.get(f"{BASE_URL}/tasks/", headers=headers)
        
        # 4. Получаем список сезонов (с вероятностью 40%)
        if random.random() < 0.4:
            requests.get(f"{BASE_URL}/seasons/", headers=headers)
        
        print(f"Пользователь {user_id} выполнил запросы")
    except Exception as e:
        print(f"Ошибка у пользователя {user_id}: {str(e)}")

def run_load_test():
    """Запуск нагрузочного тестирования"""
    print("\nНачинаем нагрузочное тестирование с 30 пользователями...")
    
    # Получаем токен админа (для простоты все пользователи будут админами)
    token = get_auth_token()
    
    # Создаем и запускаем потоки для каждого пользователя
    threads = []
    for i in range(30):
        t = Thread(target=load_test_user, args=(i+1, token))
        threads.append(t)
        t.start()
        sleep(0.1)  # Небольшой интервал между запуском пользователей
    
    # Ожидаем завершения всех потоков
    for t in threads:
        t.join()
    
    print("Нагрузочное тестирование завершено!")

if __name__ == "__main__":
    # 1. Заполняем базу данных тестовыми данными
    populate_database()
    
    # 2. Запускаем нагрузочное тестирование
    run_load_test()