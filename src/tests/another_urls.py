from django.conf import settings
from django.urls import path
from django.http import HttpResponse


from .urls import urlpatterns


def my_view(request):
    html = "<html><body>Hello World</body></html>"
    return HttpResponse(html)


if settings.ADD_HELLO_URL:
    urlpatterns += [path('another_hello/', my_view, name='another_hello'), ]
