from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views

urlpatterns = [
    # url(r'^$', views.UserList),
    # url(r'^(?P<pk>[0-9]+)/$', views.UserDetail),
    url(r'^login/$', views.CustomObtainAuthToken.as_view()),
    url(r'^sign_up/$', views.SignUp.as_view()),
    url(r'^certification/$', views.Certification.as_view()),
    url(r'^delete/(?P<pk>\d+)/$', views.Certification.as_view(), name='delete_event'),
]

urlpatterns = format_suffix_patterns(urlpatterns)