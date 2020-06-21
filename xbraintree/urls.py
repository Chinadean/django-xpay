from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views

app_name = 'braintree'
urlpatterns = [
    re_path(r'^client-token/', views.ClientTokenView.as_view(), name='client-token', ),
    re_path(r'^checkout/', views.CheckoutView.as_view(), name='checkout', ),
]
urlpatterns = format_suffix_patterns(urlpatterns)
