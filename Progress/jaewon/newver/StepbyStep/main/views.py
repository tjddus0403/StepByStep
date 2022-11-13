from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
import json

#import sys
#import os
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def home(request):
    return render(request, 'main/home.html')

def detect(request):
    return render(request, 'main/detect.html')

def qr(request):
    return render(request, 'main/qr.html')

def url(request):
    #return render(request, 'main/url.html')
    file_path="./info.json"
    with open(file_path, "r") as json_file:
        json_data=json.load(json_file)
    return render(request,'main/url.html',{"data":json_data})