from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from buskingTownServer import settings
from busking import views

urlpatterns = [

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
    url(r'^buskerPostList/(?P<pk>\d+)/$', views.BuskerPostView.as_view()),

    url(r'^likePost/$', views.LikePostView.as_view()),
    url(r'^unlikePost/(?P<pk>\d+)/$', views.LikePostView.as_view()),

    url(r'^supportCoin/$', views.supportCoinView.as_view()),
    url(r'^supportCoinDelete/(?P<pk>\d+)/$', views.supportCoinView.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)