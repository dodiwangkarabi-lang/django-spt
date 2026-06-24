"""
URL configuration for sipt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
# from rest_framework.permissions import IsAdminUser

# untuk doc
# from drf_spectacular.views import (
#     SpectacularAPIView,
#     SpectacularSwaggerView,
#     SpectacularRedocView
# )

# class AdminOnlySchemaView(SpectacularAPIView):
#     # permission_classes = [IsAdminUser]
#     pass

# class AdminOnlySwaggerView(SpectacularSwaggerView):
#     # permission_classes = [IsAdminUser]
#     pass

# class AdminOnlyRedocView(SpectacularRedocView):
#     # permission_classes = [IsAdminUser]
#     pass

urlpatterns = [
    # path("api/schema/", AdminOnlySchemaView.as_view(), name="schema"),
    # path("api/docs/", AdminOnlySwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    # path("api/redoc/", AdminOnlyRedocView.as_view(url_name="schema"), name="redoc"),
    
    path("spt/", include("spt.urls")),
    path("spt-web/", include("spt.web.urls", namespace="spt_web")),
    # path("api/spt/", include("spt.api.permohonan_api.urls", namespace="permohonan_api")),
    path("accounts/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path("api/", include("spt.api.urls", namespace="spt_api")),
    path("api/tugas/", include("tugas.api.urls", namespace="tugas_api")),
    path("spt/permohonan/", include("spt.permohonan.urls", namespace="permohonan")),
    path("workflow/disposisi/", include("workflow.disposisi.urls", namespace="disposisi")),
    path("myspt/", include("spt.spt.urls", namespace="spt")),
    path("notification/", include("notification.urls", namespace="notification")),
    path("", include("core.urls")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
