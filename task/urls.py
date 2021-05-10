from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('faqs/', views.faqs, name="faqs"),

    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    path('dashboard/', views.dashboard, name="dashboard"),
    path('worker/<str:pk_test>/', views.worker, name="worker"),
    path('user/', views.userPage, name="user-page"),
    path('tasks/', views.tasks, name="tasks"),
    path('create_task/', views.createTask, name="create_task"),
    path('update_task/<str:pk>/', views.updateTask, name="update_task"),
    path('delete_task/<str:pk>/', views.deleteTask, name="delete_task"),

]