from django.shortcuts import render
from django.http import  HttpResponse
from django.template import loader
from plotly.offline import plot
import plotly.graph_objects as go

def index(request):
    template=loader.get_template('mainPage.html')
    context={}

    return HttpResponse(template.render(context, request))
