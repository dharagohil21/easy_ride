from django.urls import include, path
from main import views

urlpatterns = [

    path('', include('rest_framework.urls')),
    path("register", views.register),
    path("login", views.login),
    path("rides", views.rides),
    path("account", views.account),

]