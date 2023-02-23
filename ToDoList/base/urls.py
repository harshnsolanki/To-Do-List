from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView
from .views import *
from django.core.exceptions import PermissionDenied

urlpatterns = [
    path('',TaskList.as_view(),name="taskList"),
    path('login',CustomLoginView.as_view(),name="login"),
    path('Registration',RegisterPage.as_view(),name="registration"),
    path('Logout',LogoutView.as_view(next_page='login'),name="logout"),
    path('tasks/<int:pk>/',TaskDetail.as_view(),name="taskDetail"),
    path('tasks-create',TaskCreate.as_view(),name="create-task"),
    path('task-update/<int:pk>/',TaskUpdate.as_view(),name="task-update"),
    path('task-delete/<int:pk>/',TaskDelete.as_view(),name="task-delete"),
]

handler404 = 'base.views.custom_page_not_found_view'
