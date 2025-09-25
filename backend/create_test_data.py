import os
import django
import datetime

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from app.models import User, Category, Task


def check_password_hashing():
    user = User.objects.get(username="testuser")

    print("🔐 Проверка хеширования паролей:")
    print(f"Пароль в базе: {user.password}")  # Хеш
    print(f"Длина хеша: {len(user.password)} символов")
    print(f"Проверка пароля 'testpass123': {user.check_password('testpass123')}")
    print(f"Проверка неверного пароля: {user.check_password('wrongpass')}")


def create_test_data():
    print("🔄 Создание тестовых данных...")

    # 1. Создаем тестового пользователя
    user, created = User.objects.get_or_create(
        username="testuser",
        defaults={"email": "test@example.com", "time_zone": "Europe/Moscow"},
    )
    if created:
        user.set_password("testpass123")  # Устанавливаем пароль
        user.save()
        print(f"✅ Создан пользователь: {user.username}")
    else:
        print(f"⚠️ Пользователь {user.username} уже существует")

    # 2. Создаем категории
    categories_data = [
        {"name": "Работа", "color": "#FF6B6B"},
        {"name": "Личное", "color": "#4ECDC4"},
        {"name": "Учеба", "color": "#45B7D1"},
        {"name": "Здоровье", "color": "#96CEB4"},
    ]

    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"], user=user, defaults={"color": cat_data["color"]}
        )
        categories.append(category)
        if created:
            print(f"✅ Создана категория: {category.name}")

    # 3. Создаем задачи
    tasks_data = [
        {
            "title": "Изучить Django ORM",
            "description": "Разобраться с моделями, миграциями и запросами",
            "status": "in_progress",
            "categories": [categories[2]],  # Учеба
        },
        {
            "title": "Сделать лабораторную работу 1",
            "description": "Выполнить ЛР1 по сетевым технологиям",
            "status": "todo",
            "categories": [categories[2]],  # Учеба
        },
        {
            "title": "Записаться на прием к врачу",
            "description": "Позвонить в поликлинику для записи",
            "status": "todo",
            "categories": [categories[3]],  # Здоровье
        },
        {
            "title": "Подготовить отчет по проекту",
            "description": "Собрать данные и оформить презентацию",
            "status": "done",
            "categories": [categories[0], categories[2]],  # Работа + Учеба
        },
    ]

    for i, task_data in enumerate(tasks_data):
        task, created = Task.objects.get_or_create(
            title=task_data["title"],
            user=user,
            defaults={
                "description": task_data["description"],
                "status": task_data["status"],
                "due_date": datetime.datetime.now() + datetime.timedelta(days=i + 1),
            },
        )

        # Добавляем категории к задаче
        for category in task_data["categories"]:
            task.categories.add(category)

        if created:
            print(f"✅ Создана задача: {task.title}")

    print("🎉 Тестовые данные созданы успешно!")
    print(f"👤 Пользователей: {User.objects.count()}")
    print(f"📂 Категорий: {Category.objects.count()}")
    print(f"📝 Задач: {Task.objects.count()}")


if __name__ == "__main__":
    # create_test_data()
    check_password_hashing()
