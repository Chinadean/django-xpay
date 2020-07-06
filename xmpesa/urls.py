from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'mpesa'
urlpatterns = [
    re_path(r'^c2b/register-url/', views.C2BRegisterURLView.as_view(), name='c2b-register-url'),
    re_path(r'^c2b/simulate/', views.C2BSimulateView.as_view(), name='c2b-simulate'),
    re_path(r'^express/', views.LNMView.as_view(), name='express'),
    re_path(r'^express/response/', views.LNMResponseView.as_view(), name='express-response'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
