from django.urls import path
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login', views.login, name = 'login'),
    path('logout', views.logout, name = 'logout'),
    path('register', views.register, name = 'register'),

    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:uid>/<str:token>/', views.reset_password, name='reset_password'),


]