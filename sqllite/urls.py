from django.contrib import admin
from django.urls import path,include
from .process.create import *

urlpatterns = [
    path('process/', DataP.as_view())
]
