from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from buskingTownServer import settings
from rentLocation import views

urlpatterns = [
    url(r'^provideAllList/$', views.ProvideAllList.as_view({'get': 'list'})),
    url(r'^provideOptionList/(?P<pk>\d+)/$', views.ProvideOptionList.as_view()),

    url(r'^provideList/(?P<pk>\d+)/$', views.ProvideView.as_view()),
    url(r'^postProvide/$', views.ProvideView.as_view()),
    url(r'^postProvideOption/$', views.ProvideOptionList.as_view()),
    url(r'^deleteProvide/(?P<pk>\d+)/$', views.ProvideView.as_view()),
    url(r'^updateProvide/(?P<pk>\d+)/$', views.ProvideView.as_view()),
    url(r'^updateProvideOption/(?P<pk>\d+)/$', views.ProvideOptionList.as_view()),

    #유저별 장소 제공 리스트
    url(r'^provideUserList/(?P<pk>\d+)/$', views.ProvideUserView.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)