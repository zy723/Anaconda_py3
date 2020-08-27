"""bookStore2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url

from book.views import index, bookList, reverse_test, LoginView

urlpatterns = [
    # url(r'^index$/', views.index, name='index'),
    #     # url(r'^bookList$/', views.bookList, name='bookList'),

    # url(r'^$', index),
    # 匹配书籍列表信息的URL,调用对应的bookList视图
    url(r'^booklist/$', bookList, name='index'),
    url(r'^testproject/$', reverse_test, name='test'),
    url(r'^(?P<value1>\d+)/(?P<value2>\d+)/$', index, name='test'),
    url(r'^login/$', LoginView.as_view(), name='login'),
]
