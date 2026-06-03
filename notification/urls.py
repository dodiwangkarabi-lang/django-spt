from django.urls import path, include

app_name = 'notification'

urlpatterns = [
    path("htmx/", include("notification.htmx.urls", namespace="notification_htmx")),
    path("api/", include("notification.api.urls", namespace="notification_api")),
    path("", include("notification.web.urls", namespace="notification_web")),
]