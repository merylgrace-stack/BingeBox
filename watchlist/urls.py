from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/media/',views.media_list, name='media-list'),
    path('api/media/<int:pk>/', views.media_detail, name='media-detail'),
    path('api/test/', views.api_test, name='api_test'),
]