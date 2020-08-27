from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.generic.base import View


def index(request, value1, value2):
    print(value1, value2)
    # return HttpResponse("hahah")
    context = {'v1': value2, 'v2': value1}
    return render(request, 'index.html', context=context)


def bookList(request):
    return HttpResponse('ok')


def reverse_test(request):
    url = reverse("book:index")
    return HttpResponse(url)


class LoginView(View):

    def get(self, request):
        userName = request.GET.get('userName')
        passWd = request.GET.get('passWd')

        # return HttpResponse('你好' + userName + ',你的密码为:' + passWd)
        # return JsonResponse({'userName': userName, 'passWd': passWd})
        # path = reverse('book:index')
        # return redirect(path)
        # request.set_cookie('userName', userName)

        # return JsonResponse({'userName': userName, 'passWd': passWd})

        response = JsonResponse({'userName': userName, 'passWd': passWd})
        response.set_cookie('userName', userName, max_age=3600)

        return response

    def post(self, request):
        userName = request.POST.get('userName')
        passWd = request.POST.get('passWd')

        return HttpResponse('你好' + userName + ',你的密码为:' + passWd)
