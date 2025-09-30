from django.shortcuts import render

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

    """@action(detail=False, methods=["post"], permission_classes=[permissions.AllowAny])
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
"""


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
