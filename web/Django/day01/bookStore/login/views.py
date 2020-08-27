from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
"""
视图函数

"""


def index(request):
    return HttpResponse("index")
