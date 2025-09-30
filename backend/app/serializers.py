from rest_framework import serializers
from .models import User, Category, Task


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "time_zone", "date_joined", "password"]
        read_only_fields = ["id", "date_joined"]

    def create(self, validated_data):

        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "color", "user", "created_at"]
        read_only_fields = ["id", "user", "created_at"]


class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Category.objects.all(), source="categories", write_only=True
    )

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "due_date",
            "created_at",
            "updated_at",
            "user",
            "categories",
            "category_ids",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
