from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns= [
    path('register/', views.register, name= "register"),
    path('register/<str:ref_by>', views.register, name= "register"),
    path('signin/', views.custom_login, name= "signin"),
    path('signin/<str:ref_by>', views.custom_login, name= "signin"),
    path('logout/', views.logout, name= "logout")
]