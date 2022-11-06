from django.shortcuts import render
from django.http import HttpResponse
import sys
import os
# 상위 폴더 내의 파일 참조 (절대경로를 path에 추가)
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def home(request):
    return render(request, 'home/home.html')