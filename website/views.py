from django.shortcuts import render
from django.http import  HttpResponse
import os

cwd = os.getcwd()
print(cwd)





def index(request):
    return render(request,'index.html')
