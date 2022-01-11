from django.urls import path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns =  [
    path('home',views.clients,name='clients'),
    path('results', views.results,name='results'),
    path('factu', views.factu,name='factu'),
    path('mde', views.mde, name='mde'),
    path('mobilite', views.mobi, name='mobilite'),
    path('bilan', views.bilan, name='bilan')
]
urlpatterns += staticfiles_urlpatterns()

