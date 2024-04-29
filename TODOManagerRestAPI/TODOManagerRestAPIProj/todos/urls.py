from django.urls import path
from .views import project_list, project_detail, todo_list, todo_detail, mark_todo_as_done
from .import views


urlpatterns = [
    path('api/projects/', project_list),
    path('api/projects/<int:id>/', project_detail),
    path('api/todos/', todo_list),
    path('api/todos/<int:id>/', todo_detail),
    path('api/todos/<int:id>/mark_as_done/', mark_todo_as_done),
    path("api/user/signup/", views.SignupAPIView.as_view(), name="user-signup"),
    path("api/user/signin/", views.SigninAPIView.as_view(), name="user-signin"),
]
