from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('analytics/', views.analytics, name='analytics'),
    path('<str:code>/', views.redirect_to_original, name='redirect'),
]