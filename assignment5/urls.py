from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse


def healthz(_request):
    return HttpResponse('ok', content_type='text/plain', status=200)


urlpatterns = [
path('admin/', admin.site.urls),
path('', include('puzzle.urls')),
path('healthz', healthz), # ALB health check
]