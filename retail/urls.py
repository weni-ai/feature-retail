"""
URL configuration for retail project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.views.static import serve
from django.conf import settings
from django.urls import re_path
from django.shortcuts import redirect
from rest_framework import routers

from retail.healthcheck import views
from retail.projects import views as project_views

router = routers.SimpleRouter()
router.register("projects", project_views.ProjectViewSet, basename="project")


urlpatterns = [
    path("", lambda _: redirect("admin/", permanent=True)),
    path("admin/", admin.site.urls),
    path("healthcheck/", views.healthcheck, name="healthcheck"),
    path("api/", include(router.urls)),
]

urlpatterns.append(
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT})
)
