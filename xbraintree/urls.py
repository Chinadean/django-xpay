from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'braintree'
urlpatterns = [
]
urlpatterns = format_suffix_patterns(urlpatterns)
