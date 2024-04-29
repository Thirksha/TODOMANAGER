from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http import JsonResponse, HttpResponse
from .serializers import ProjectSerializer, TodoSerializer, SignupSerializer
from .models import Project, Todo
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SigninSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

# Create your views here.

class SignupAPIView(APIView):
    def post(self, request):
        serializer = SignupSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            res = { 'status': status.HTTP_201_CREATED }
            return Response(res, status=status.HTTP_201_CREATED )
        else:
            res = { 'status' : status.HTTP_400_BAD_REQUEST, 'data':serializer.errors }
            return Response(res, status= status.HTTP_400_BAD_REQUEST)


class SigninAPIView(APIView):
    def post(self, request):
        serializer = SigninSerializer(data = request.data)
        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                token = Token.objects.get(user=user)
                response = {
                    "status": status.HTTP_200_OK,
                    "message": "success",
                    "data": {
                        "Token": token.key
                           }
                    }
                return Response(response, status = status.HTTP_200_OK)
            else:
                response = {
                    "status": status.HTTP_401_UNAUTHORIZED,
                    "message": "Invalid Email or Password",
                }
                return Response(response, status = status.HTTP_401_UNAUTHORIZED)
        response = {
            "status":status.HTTP_400_BAD_REQUEST,
            "message": "bad request",
            "data": serializer.errors
        }
        return Response(response, status = status.HTTP_400_BAD_REQUEST)



@csrf_exempt
def project_list(request):
    if request.method == "GET":
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
def project_detail(request, id):
    try:
        project = Project.objects.get(pk=id)
    except Project.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = ProjectSerializer(project)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = ProjectSerializer(project, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        project.delete()
        return HttpResponse(status=204)


@csrf_exempt
def todo_list(request):
    if request.method == "GET":
        todos = Todo.objects.all()
        serializer = TodoSerializer(todos, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = TodoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)




@csrf_exempt
@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
def todo_detail(request, id):
    try:
        todo = Todo.objects.get(pk=id)
    except Todo.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = TodoSerializer(todo)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = TodoSerializer(todo, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == "DELETE":
        todo.delete()
        return HttpResponse(status=204)


@csrf_exempt
@api_view(['GET','PUT','DELETE'])
@permission_classes((IsAuthenticated, ))
def mark_todo_as_done(request, id):
    try:
        todo = Todo.objects.get(pk=id)
    except Todo.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "PUT":
        # Mark the todo as done
        todo.completed = True
        todo.save()
        serializer = TodoSerializer(todo)
        return JsonResponse(serializer.data)
    else:
        return HttpResponse(status=400)