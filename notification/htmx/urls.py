from django.urls import path

from . import views

app_name = 'notification_htmx'

urlpatterns = [
    path("list/", views.list_view, name="list"),
    path("notifikasi-navbar/", views.notifikasi_navbar, name="notifikasi_navbar"),
]