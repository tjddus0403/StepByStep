from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
import json

def home(request):
    return render(request, 'main/home.html')

def detect(request):
    return render(request, 'main/detect.html')

def qr(request):
    return render(request, 'main/qr.html')

def url(request):
    # 최종적으로 사용자에게 보여주는 정보담은 result.json 데이터 전달
    file_path="./result.json"
    with open(file_path, "r") as json_file:
        json_data=json.load(json_file)
    return render(request,'main/url.html',{"data":json_data})