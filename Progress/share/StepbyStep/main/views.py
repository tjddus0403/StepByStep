from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics

#import sys
#import os
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

def home(request):
    return render(request, 'main/home.html')

def detect(request):
    return render(request, 'main/detect.html')