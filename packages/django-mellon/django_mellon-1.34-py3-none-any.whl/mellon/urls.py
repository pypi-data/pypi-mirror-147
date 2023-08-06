import django
from django.urls import re_path

from . import views

urlpatterns = [
    re_path('login/$', views.login, name='mellon_login'),
    re_path('login/debug/$', views.debug_login, name='mellon_debug_login'),
    re_path('logout/$', views.logout, name='mellon_logout'),
    re_path('metadata/$', views.metadata, name='mellon_metadata'),
]
