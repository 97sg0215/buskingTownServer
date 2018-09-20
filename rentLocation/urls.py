from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from buskingTownServer import settings
from rentLocation import views

urlpatterns = [
    url(r'^provideList/$', views.Provide_View.as_view({'get': 'list'})),
    #제공장소 삭제
    url(r'^deleteProvide/(?P<pk>\d+)/$', views.ProvideView.as_view()),
    #제공장소 옵션이랑 같이 확인 url
    url(r'^provideDetail/(?P<pk>\d+)/$', views.ProvideList.as_view()),
    #제공장소 수정
    url(r'^provideUpDate/(?P<pk>\d+)/$', views.ProvideView.as_view()),
    #제공장소 업로드
    url(r'^provideUpload/$', views.ProvideList.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)