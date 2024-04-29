from django.contrib import admin
from .models import Project, Todo
from rest_framework.authtoken.models import Token

# Register your models here.
admin.site.register(Token)
admin.site.register(Project)
admin.site.register(Todo)
