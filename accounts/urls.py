from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_view, name="accounts_login"),
    path("change_password/", views.change_password, name="accounts_change_password"),
    path("logout/", views.logout_view, name="accounts_logout"),
    path("register/", views.register, name="accounts_register"),
]