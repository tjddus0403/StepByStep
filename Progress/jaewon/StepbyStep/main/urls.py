from django.urls import path
from django.http import StreamingHttpResponse
from camera import VideoCamera, gen
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('detect/', views.detect, name='detect'),
    path('camera/', lambda r: StreamingHttpResponse(gen(VideoCamera()),
                                                    content_type='multipart/x-mixed-replace; boundary=frame')),
    path('qr/', views.qr, name='qr'),
    path('url/', views.url, name='url'),
]