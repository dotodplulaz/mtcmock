from django.contrib import admin
from django.urls import path,include
from django.conf import settings
# from motcors import views

from django.views.static import serve
#from django.conf.urls import url
from . import views
from django.conf.urls.static import static

urlpatterns = [
         #START OF URLS IN ACCOUNT
    path('', views.index,name='index'),
    path('home/', views.home,name='home'), 
    path('logout/', views.logout,name='logout'),
    path('upload/', views.upload,name='upload'),
    path('marks/', views.marks,name='marks'),
    path('results/', views.results,name='results'),
    path('bestandpoor/', views.bestandpoor,name='bestandpoor'),
    path('bestandpoorupload/', views.bestandpoorupload,name='bestandpoorupload'),
 
]
