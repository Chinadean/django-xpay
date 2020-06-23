from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'mpesa'
urlpatterns = [
    re_path(r'lnm/', views.LNMView.as_view(), name='lnm'),
    re_path(r'lnm/response/', views.LNMResponseView.as_view(), name='lnm-response'),
]
urlpatterns = format_suffix_patterns(urlpatterns)
