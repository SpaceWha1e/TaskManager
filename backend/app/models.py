from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


# Модель пользователя
class User(AbstractUser):
    # AbstractUser уже содержит: username, email, password, first_name, last_name
    time_zone = models.CharField(max_length=50, default="UTC")

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name="groups",
        blank=True,
        help_text="The groups this user belongs to.",
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name="user permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_name="custom_user_set",
        related_query_name="user",
    )

    def __str__(self):
        return self.username


# Модель категории
class Category(models.Model):
    # UUID вместо обычного ID - более безопасно
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)  # название категории
    color = models.CharField(max_length=7, default="#000000")  # цвет в формате HEX
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # владелец категории
    created_at = models.DateTimeField(auto_now_add=True)  # дата создания

    class Meta:
        ordering = ["name"]  # сортировка по имени

    def __str__(self):
        return self.name


# Модель задачи
class Task(models.Model):
    # Выбор статуса задачи
    STATUS_CHOICES = [
        ("todo", "To Do"),
        ("in_progress", "In Progress"),
        ("done", "Done"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)  # заголовок задачи
    description = models.TextField(blank=True)  # описание (необязательное)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="todo")
    due_date = models.DateTimeField(null=True, blank=True)  # срок выполнения
    created_at = models.DateTimeField(auto_now_add=True)  # дата создания
    updated_at = models.DateTimeField(auto_now=True)  # дата обновления

    # Связь с пользователем (владельцем задачи)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Связь многие-ко-многим с категориями
    categories = models.ManyToManyField(Category, related_name="tasks", blank=True)

    class Meta:
        ordering = ["-created_at"]  # новые задачи сначала

    def __str__(self):
        return self.title
