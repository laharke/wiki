from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry_page, name="entry_page"),
    path("serach", views.search, name="search"),
    path("newpage", views.new_page, name="new_page"),
    path("editentry", views.edit_entry, name="edit_entry"),
    path("randompage", views.random_page, name="random_page")
]
