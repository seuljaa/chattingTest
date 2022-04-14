from django.urls import path
from chatting import views

urlpatterns = [
    path('' , views.main , name='main'),
]