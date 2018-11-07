# 클래스 기반의 Rest CRUD 처리
import operator
from itertools import chain

from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.generics import UpdateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView

from accounts.serializers import *
from rest_framework import viewsets, status, filters
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics
from django.core.exceptions import ObjectDoesNotExist
from pusher_push_notifications import PushNotifications

from accounts.permissions import IsAuthenticatedOrCreate
from django.contrib.auth.models import User
from drf_multiple_model.views import ObjectMultipleModelAPIView, FlatMultipleModelAPIView
from django.db.models import Sum, F, Q

# generics 에 목록과 생성 API 가 정의되어 있다
from busking.models import Post, supportCoin
from busking.serializers import LikePostSerializer, SupportCoinSerializer
from rentLocation.serializers import ReservationPracticeRoomSerializer


class UserList(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# generics 에 상세, 수정, 삭제 API가 정의되어 있다
class UserDetail(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

class DeleteUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrCreate,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserDetailEdit(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    parser_classes = (MultiPartParser,)
    permission_classes = (IsAuthenticatedOrCreate,)

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        Profile = self.get_object(pk)
        serializer = ProfileSerializer(Profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BuskerList(viewsets.ModelViewSet):
    queryset = Busker.objects.all()
    serializer_class = BuskerSerializer

class ConnectionList(viewsets.ModelViewSet):
    queryset = Connections.objects.all()
    serializer_class = ConnectionsSerializer

class ConnectionsView(generics.CreateAPIView):
    queryset = Connections.objects.all()
    serializer_class = ConnectionsSerializer

    def get_object(self, pk):
        try:
            return Connections.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = ConnectionsSerializer(event)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = ConnectionsSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ScoreListView(generics.ListAPIView):
    queryset = Busker.objects.filter(busker_type=1, certification=True).prefetch_related('friend_set', 'likes').annotate(
        score=models.F('received_coin') + models.Count('friend_set__following_id') + models.Count('likes')).order_by('-score')
    serializer_class = ScoreSerializer

class FollowerList(APIView):
    def get_object(self, pk):
        try:
            return Busker.objects.get(pk=pk)
        except Busker.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        followers = event.get_followers()
        serializer = ConnectionsSerializer(followers, many=True)
        return Response(serializer.data)

class FollowingList(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk,format=None):
        event = self.get_object(pk)
        followings = event.get_followings()
        serializer = ConnectionsSerializer(followings, many=True)
        return Response(serializer.data)

class FollowingList(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk,format=None):
        event = self.get_object(pk)
        followings = event.get_followings()
        serializer = ConnectionsSerializer(followings, many=True)
        return Response(serializer.data)

class LikeCheckList(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk,format=None):
        event = self.get_object(pk)
        liked = event.get_liked()
        serializer = LikePostSerializer(liked, many=True)
        return Response(serializer.data)


class CoinList(APIView):
    def get_object(self, pk):
        try:
            return Busker.objects.get(pk=pk)
        except Busker.DoesNotExist:
            raise Http404

    def get(self, request, pk,format=None):
        event = self.get_object(pk)
        coin = event.get_coin()
        serializer = SupportCoinSerializer(coin, many=True)
        return Response(serializer.data)

class PurchaseCoinView(generics.CreateAPIView):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseCoinSerializer

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        coin = event.get_purchase_coin()
        serializer = PurchaseCoinSerializer(coin, many=True)
        return Response(serializer.data)

class SendCoinList(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk,format=None):
        event = self.get_object(pk)
        coin = event.get_post_coin()
        serializer = SupportCoinSerializer(coin, many=True)
        return Response(serializer.data)

class PracticeList(APIView):
    def get_object(self, pk):
        try:
            return Busker.objects.get(pk=pk)
        except Busker.DoesNotExist:
            raise Http404

    def get(self, request, pk,format=None):
        event = self.get_object(pk)
        room = event.get_practice_reservation()
        serializer = ReservationPracticeRoomSerializer(room, many=True)
        return Response(serializer.data)



#이미지 전송을 위해 json형식이 아닌 formparser로 데이터 전송
class BuskerView(generics.CreateAPIView):
    queryset = Busker.objects.all()
    serializer_class = BuskerSerializer
    parser_classes = (MultiPartParser,)

    #busker_id로 버스커 객체 얻어옴
    def get_object(self, pk):
        try:
            return Busker.objects.get(pk=pk)
        except Busker.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = BuskerSerializer(event)
        return Response(serializer.data)

    #버스커 객체 생성
    def post(self, request, *args, **kwargs):
        serializer_class = BuskerSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        Busker = self.get_object(pk)
        serializer = BuskerSerializer(Busker, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #버스커 객체 삭제
    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#회원가입 뷰 권한 처리를 위해 permission
class SignUp(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = (IsAuthenticatedOrCreate,)

#토큰 받아오는 뷰
class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])

        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        return Response({'token': token.key, 'id': token.user_id, 'username': user.username, 'email': user.email,
                         'user_phone': user.profile.user_phone
                         })

class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticatedOrCreate,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
        # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response("Success.", status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCoinManagement(FlatMultipleModelAPIView):
    sorting_fields = ['-date_created']
    def get_querylist(self):
        user = self.kwargs['user']
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']

        querylist = [
            {'queryset': Purchase.objects.filter(user=user, date_created__gte=start_date, date_created__lte=end_date), 'serializer_class': PurchaseCoinSerializer, 'label': 'purchase'},
            {'queryset': supportCoin.objects.filter(user=user, date_created__gte=start_date, date_created__lte=end_date), 'serializer_class': SupportCoinSerializer, 'label': 'support'}
        ]
        return querylist


#
# def push_notify(data):
#     pn_client = PushNotifications(
#         instance_id='4c4a8894-87b8-4006-8e7e-b2b57fa83b79',
#         secret_key='3A16D47264DFF2A3D50223DA373AB12A0D70924121B9CF6E98FEDB723F16C91B',
#     )
#
#     response = pn_client.publish(
#         interests=['hello'],
#         publish_body={'apns': {'aps': {'alert': 'follow'}},
#                       'fcm': {'notification': {'title': 'test', 'body': str(data)}}}
#     )
#
#     print(response['publishId'])