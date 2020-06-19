from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'stripe'
urlpatterns = [
    re_path(r'^client-secret/', views.ClientSecretView.as_view(), name='client-secret', ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
