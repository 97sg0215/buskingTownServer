from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from accounts import views
from django.conf.urls.static import static
from buskingTownServer import settings

urlpatterns = [
    #로그인 및 회원가입 url
    url(r'^login/$', views.CustomObtainAuthToken.as_view()),
    url(r'^sign_up/$', views.SignUp.as_view()),
    #비밀번호 변경
    url(r'^changePassword/(?P<pk>\d+)/$', views.ChangePasswordView.as_view()),
    #회원탈퇴
    url(r'^deleteUser/(?P<pk>\d+)/$', views.DeleteUserView.as_view()),

    #회원 이미지 업로드
    url(r'^update_profile/(?P<pk>\d+)/$', views.UserDetailEdit.as_view()),

    #팔로우 전체 목록
    url(r'^allFollowList/$', views.ConnectionList.as_view({'get': 'list'})),
    #각 버스커 별 팔로워 목록
    url(r'^followerList/(?P<pk>\d+)/$', views.FollowerList.as_view()),
    #각 유저 별 팔로잉 목록
    url(r'^followingList/(?P<pk>\d+)/$', views.FollowingList.as_view()),
    #팔로잉
    url(r'^following/$', views.ConnectionsView.as_view()),
    #팔로잉 삭제
    url(r'^unfollowing/(?P<pk>\d+)/$', views.ConnectionsView.as_view()),

    #게시물 좋아요 체크
    url(r'^likeCheck/(?P<pk>\d+)/$', views.LikeCheckList.as_view()),

    #버스커 인증 url
    url(r'^certification/$', views.BuskerView.as_view()),
    #버스커 객체 삭제 url 인증 실패시 자동으로 실행되게 안드로이드에 설정
    url(r'^delete/(?P<pk>\d+)/$', views.BuskerView.as_view()),
    #버스커확인 url
    url(r'^buskerDetail/(?P<pk>\d+)/$', views.BuskerView.as_view()),

    #버스커 랭킹 정렬
    url(r'^buskerRank/$', views.ScoreListView.as_view()),

    #받은 코인 리스트
    url(r'^coin/(?P<pk>\d+)/$', views.CoinList.as_view())

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = format_suffix_patterns(urlpatterns)