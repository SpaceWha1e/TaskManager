from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from .models import User, Category, Task
from .serializers import UserSerializer, CategorySerializer, TaskSerializer


# Auth functions
@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = User.objects.create_user(
            username=serializer.validated_data["username"],
            email=serializer.validated_data.get("email", ""),
            password=request.data.get("password"),
            time_zone=serializer.validated_data.get("time_zone", "UTC"),
        )
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return Response(
            {"message": "Login successful", "user": UserSerializer(user).data}
        )
    return Response(
        {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(["POST"])
def logout_user(request):
    logout(request)
    return Response({"message": "Logout successful"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "username"

    @action(detail=True, methods=["get"])
    def profile(self, request, username=None):
        user = self.get_object()
        return Response(UserSerializer(user).data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    # временное решение
    def perform_create(self, serializer):
        # Автоматически назначаем первого пользователя как владельца
        # Позже заменим на текущего аутентифицированного пользователя
        user = User.objects.first()
        if user:
            serializer.save(user=user)
        else:
            # Если нет пользователей, создаем задачу без пользователя (временно)
            serializer.save()

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None):
        category = self.get_object()
        tasks = category.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]

    # Временное решение
    def perform_create(self, serializer):
        # Автоматически назначаем первого пользователя как владельца
        # Позже заменим на текущего аутентифицированного пользователя
        user = User.objects.first()
        if user:
            serializer.save(user=user)
        else:
            # Если нет пользователей, создаем задачу без пользователя (временно)
            serializer.save()

    @action(detail=True, methods=["get"])
    def categories(self, request, pk=None):
        task = self.get_object()
        categories = task.categories.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


"""from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import User, Category, Task
from .serializers import UserSerializer, CategorySerializer, TaskSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    """ """@action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data.get("email", ""),
                password=request.data.get("password"),
                time_zone=serializer.validated_data.get("time_zone", "UTC"),
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
""" """


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny] 

    def get_queryset(self):
        return Category.objects.all()


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny] 

    def get_queryset(self):
        return Task.objects.all()

    @action(detail=True, methods=["post"])
    def add_category(self, request, pk=None):
        task = self.get_object()
        category_id = request.data.get("category_id")
        try:
            category = Category.objects.get(id=category_id)
            task.categories.add(category)
            return Response({"status": "category added"})
        except Category.DoesNotExist:
            return Response(
                {"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND
            )
"""


"""from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import User, Category, Task
from .serializers import UserSerializer, CategorySerializer, TaskSerializer


class AuthViewSet(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data["username"],
                email=serializer.validated_data.get("email", ""),
                password=request.data.get("password"),
                time_zone=serializer.validated_data.get("time_zone", "UTC"),
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {"message": "Login successful", "user": UserSerializer(user).data}
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )

    def logout(self, request):
        logout(request)
        return Response({"message": "Logout successful"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = "username"  # для поиска по username вместо id

    @action(detail=True, methods=["get"])
    def profile(self, request, username=None):
        user = self.get_object()
        return Response(UserSerializer(user).data)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["get"])
    def tasks(self, request, pk=None):
        category = self.get_object()
        tasks = category.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["get"])
    def categories(self, request, pk=None):
        task = self.get_object()
        categories = task.categories.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)"""
