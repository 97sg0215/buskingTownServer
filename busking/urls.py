from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from busking import views

urlpatterns = [
    #버스커 랭킹 url
    url(r'^buskerRank/$', views.BuskerRank),
]

urlpatterns = format_suffix_patterns(urlpatterns)