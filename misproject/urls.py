"""
URL configuration for misproject project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from misapi import views as misapi_views
from misapp import views as misapp_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api_patients', misapi_views.api_patients, name='api_patients'),
    path('api_patients/<id_patient>', misapi_views.api_patients, name='api_patients'),
    path('api_passports', misapi_views.api_passports, name='api_passports'),
    path('api_addresses', misapi_views.api_addresses, name='api_addresses'),
    path('api_organizations', misapi_views.api_organizations, name='api_organizations'),
    path('api_managers', misapi_views.api_managers, name='api_managers'),
    path('api_licenses', misapi_views.api_licenses, name='api_licenses'),

    path('', misapp_views.main, name='main'),
    path('patient_search', misapp_views.patient_search, name='patient_search'),
    path('patients/<id_patient>', misapp_views.patients, name='patients')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
