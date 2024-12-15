# API для управління подіями

## Огляд

Це REST API, розроблене на основі Django, для управління подіями, такими як конференції, зустрічі чи воркшопи. Користувачі можуть створювати, переглядати, оновлювати та видаляти події, а також реєструватися на них. Проєкт підтримує базову реєстрацію та аутентифікацію користувачів.

---

## Можливості

- **CRUD для подій**: створення, читання, оновлення та видалення подій.
- **Аутентифікація користувачів**: захищений доступ через JWT-токени.
- **Реєстрація на події**: користувачі можуть реєструватися на події та переглядати свої реєстрації.
~~- **Підтримка Docker**: повна контейнеризація через Docker та Docker Compose.~~
- **База даних**: SQLite для надійного зберігання даних.

### Додаткові функції
- Фільтрація подій за датою, місцем та організатором.
- Надсилання email-сповіщень про реєстрацію на події.

---

## Як розпочати

### Передумови

- Базові знання Python і Django.

### Інсталяція

1. Клонуйте репозиторій:
   ```bash
   git clone https://github.com/batraktar/event_management.git
   cd event_management
2. Створіть та активуйте віртуальне середовище:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Для Windows: venv\Scripts\activate
3. Встановіть залежності:
   ```bash
   pip install -r requirements.txt
4. Застосуйте міграції:
   ```bash
   python manage.py migrate
5. Створіть адміністратора:
   ```bash
   python manage.py createsuperuser
6. Запустіть сервер:
   ```bash
   python manage.py runserver
7. API буде доступне за адресою http://127.0.0.1:8000.


# API для управління подіями

## API-ендпоінти

### Аутентифікація
- **POST** `/api/token/`  
  Отримання JWT-токенів.
  **Тіло запиту**:
  ```json
  {
    "username": "your_username",
    "password": "your_password"
  } 
  ```
   **Відповідь**:
   ```json
   {
     "access": "jwt_access_token",
     "refresh": "jwt_refresh_token"
   }
  ```
  
- **POST** `/api/token/refresh/`
Оновлення токену доступу.
**Тіло запиту**:
```json
{
  "refresh": "your_refresh_token"
}
```
**Відповідь**:
```json
{
  "access": "new_jwt_access_token"
}
```
### Реєстрація користувача
- **POST** `/api/register/`
   Реєстрація нового користувача.
   **Тіло запиту**:
```json
{
  "username": "new_username",
  "password": "new_password"
}
```
   **Відповідь**:
```json
{
  "message": "User created successfully"
}
```
### Події
- **GET** `/api/events/`
Отримання списку всіх подій.
**Відповідь**:
```json
[
  {
    "id": 1,
    "title": "Event Title",
    "description": "Event Description",
    "date": "2024-12-20T15:00:00Z",
    "location": "Event Location",
    "organizer": "username"
  }
]
```
- **POST** `/api/events/`
Створення нової події (доступно тільки для авторизованих користувачів).
**Тіло запиту**:
```json
{
  "title": "New Event",
  "description": "Description of the event",
  "date": "2024-12-20T15:00:00Z",
  "location": "Location"
}
```
**Відповідь**:
```json
{
  "id": 1,
  "title": "New Event",
  "description": "Description of the event",
  "date": "2024-12-20T15:00:00Z",
  "location": "Location",
  "organizer": "username"
}
```
- **GET** `/api/events/<id>/`
Отримання деталей події.
**Відповідь**:
```json
{
  "id": 1,
  "title": "Event Title",
  "description": "Event Description",
  "date": "2024-12-20T15:00:00Z",
  "location": "Event Location",
  "organizer": "username"
}
```