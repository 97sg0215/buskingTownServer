from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from buskingTownServer import settings
from busking import views

urlpatterns = [
    #버스커 랭킹 url
    url(r'^buskerRank/$', views.BuskerRank),

    ### 이곳에 들어가는 pk는 포스트 id임 ###
    #게시물 업로드 url
    url(r'^postUpload/$', views.PostView.as_view()),
    #게시물 삭제 url
    url(r'^postDelete/(?P<pk>\d+)/$', views.PostView.as_view()),
    #게시물 상세 url
    url(r'^postDetail/(?P<pk>\d+)/$', views.PostView.as_view()),
    #게시물 리스트 url
    url(r'^postList/$', views.PostList.as_view({'get': 'list'})),
    #게시물 수정 url
    url(r'postUpdate/(?P<pk>\d+)/$', views.PostView.as_view()),

    ### 이곳에 들어가는 pk는 버스커 id임 ###
    #각 버스커 별 팔로워 목록
    url(r'^buskerPostList/(?P<pk>\d+)/$', views.BuskerPostView.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)