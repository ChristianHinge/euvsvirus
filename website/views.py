from django.shortcuts import render
from django.http import  HttpResponse
import os

from website import *




def index(request):
    return render(request,'index.html')
