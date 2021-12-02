from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('', views.clients),
    path('base', views.base)
]

urlpatterns += staticfiles_urlpatterns()
