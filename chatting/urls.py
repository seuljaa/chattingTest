from django.urls import path
from chatting import views

urlpatterns = [
    path('', views.main, name='main'),
    path('<str:room_name>/', views.room, name='room'),
]