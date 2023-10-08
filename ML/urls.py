from django.urls import path
from . import views


urlpatterns = [


    path('', views.home, name = 'home'),
    path('home', views.home, name = 'home'),
    path('contact', views.contact, name = 'contact'),

    path('textblob/<str:keyword>/', views.textblob_view, name='textblob_view'),
    path('vader/<str:keyword>/', views.vader_view, name='vader_view'),
    path('bert1/<str:keyword>/', views.bert1_view, name='bert1_view'),
    # path('bert3/<str:keyword>/', views.bert3_view, name='bert3_view'),

    
    path('distilledberta/<str:keyword>/', views.distilledberta_view, name='distilledberta_view'),
    # path('roberta2/<str:keyword>/', views.roberta2_view , name='roberta1_view'),
    
]
views.s