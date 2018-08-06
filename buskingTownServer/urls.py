"""buskingTown URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.conf.urls import url, include
from rest_framework import routers
from accounts import views
from buskingTownServer import settings

router = routers.DefaultRouter()
router.register(r'user', views.UserList)
router.register(r'userdetail', views.UserDetail)

urlpatterns = [

    url(r'^admin/', admin.site.urls),

    # 사용자, 그룹목록 처리를 위한 url - 위의 router에서 처리되어 있다
    url(r'^', include(router.urls)),

    # 인증처리를 위한 url
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    #로그인,회원가입 등의 사용자 관리 url
    url(r'^accounts/', include('accounts.urls')),

    url(r'^busking/', include('busking.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
