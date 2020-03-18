import json

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic.base import View


class IndexView(View):
    def get(self, request):
        return render(request, 'login.html')


class LoginView(View):

    def get(self, request):
        data = request.GET
        username = data.get('username')
        password = data.get('password')
        return JsonResponse({'info': {'username': username}})

    def post(self, request):
        # data = request.POST
        data = json.loads(request.body.decode())
        username = data.get('username')
        password = data.get('password')
        return JsonResponse({'info': {'username': username}})
