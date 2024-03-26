from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("uploadFile/", views.uploadFile, name="uploadFile"),
    path("search/", views.search, name="search"),
    path("result/", views.result, name="result"),
    path("countWords/", views.countWords, name="countWords")
]
