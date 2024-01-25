from django.urls import path
from . import views


urlpatterns = [


    path('', views.landing, name = 'landing'),
    path('home', views.home, name = 'home'),
    path('contact', views.contact, name = 'contact'),
    path('donate', views.donate, name = 'donate'),

    path('textblob/<str:keyword>/', views.textblob_view, name='textblob_view'),
    path('vader/<str:keyword>/', views.vader_view, name='vader_view'),
]

