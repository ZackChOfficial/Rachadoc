"""rachadoc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include, re_path
from django.conf import settings

urlpatterns = [
    path("overseas/", admin.site.urls),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r"^rosetta/", include("rosetta.urls"))]

urlpatterns += [
    re_path(r"^v1/accounts/", include(("accounts.urls", "accounts"), namespace="accounts-v1")),
    re_path(r"^v1/agendasetting/", include(("agendasetting.urls", "agendasetting"), namespace="agendasetting-v1")),
    re_path(r"^v1/clinic/", include(("clinic.urls", "clinic"), namespace="clinic-v1")),
    re_path(r"^v1/common/", include(("common.urls", "common"), namespace="common-v1")),
    re_path(r"^v1/events/", include(("events.urls", "events"), namespace="events-v1")),
]
