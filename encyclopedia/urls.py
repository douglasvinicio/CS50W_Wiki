from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create", views.create, name="create"),
    path("search", views.search, name="search"),
    path("<str:name>", views.showPage, name="showPage"),
    path("<str:name>/edit", views.edit, name="edit"),
]
