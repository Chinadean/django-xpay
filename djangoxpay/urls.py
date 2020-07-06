"""djangoxpay URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import include, re_path

urlpatterns = [
    re_path(r'^accounts/', include('xauth.urls', namespace='xauth')),
    re_path(r'^stripe/', include('xstripe.urls', namespace='stripe')),
    re_path(r'^square/', include('xsquare.urls', namespace='square')),
    re_path(r'^braintree/', include('xbraintree.urls', namespace='braintree')),
    re_path(r'^mpay/', include('xmpesa.urls', namespace='mpesa')),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^admin-api/', include('rest_framework.urls', namespace='rest_framework')),
]
