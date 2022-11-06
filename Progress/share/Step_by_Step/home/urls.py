from django.urls import path
from django.http import StreamingHttpResponse
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
]