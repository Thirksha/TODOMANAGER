from rest_framework import serializers
from .models import Project, Todo
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password


class SignupSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        return super(SignupSerializer,self).create(validated_data)
    class Meta:
        model = User
        fields = ['username', 'password']

class SigninSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = User
        fields = ['username', 'password']

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    todos = TodoSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
