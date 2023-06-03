from django.urls import path 
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home, name="home"),
    path('home', views.home, name="home"),
    path('sign-up', views.sign_up, name="sign_up"),
    path('login/', auth_views.LoginView.as_view(template_name='./html/login.html'), name='login'),
    path('dashboard', views.dashboard, name="dashboard"),
    path('create', views.create, name="create"),
    path('join', views.join, name="join"),
    path('judges', views.data, name="data"),
    path('charge/', views.charge, name="charge"),
]
