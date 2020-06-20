from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'square'
urlpatterns = [
    re_path(r'^confirm-payment/', views.PaymentView.as_view(), name='confirm-payment', ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
