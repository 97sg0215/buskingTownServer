from django.db.models import Count
from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from accounts import models
from accounts.models import Busker
from busking.models import Post, LikePost, supportCoin, RoadConcert
from busking.serializers import PostSerializer, LikePostSerializer, SupportCoinSerializer, RoadConcertSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets, status


class BuskerPostView(APIView):
    def get_object(self, pk):
        try:
            return Busker.objects.get(pk=pk)
        except Busker.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        posts = event.get_posts()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

#게시물 작성 뷰
class PostView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = (MultiPartParser,)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = PostSerializer(event)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = PostSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    #업데이트 메소드
    def put(self, request, pk, format=None):
        Post = self.get_object(pk)
        serializer = PostSerializer(Post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostList(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class LikePostView(generics.CreateAPIView):
    queryset = LikePost.objects.all()
    serializer_class = LikePostSerializer

    def get_object(self, pk):
        try:
            return LikePost.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = LikePostSerializer(event)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = LikePostSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class supportCoinView(generics.CreateAPIView):
    queryset = supportCoin.objects.all()
    serializer_class = SupportCoinSerializer

    def get_object(self, pk):
        try:
            return supportCoin.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = SupportCoinSerializer(event)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = SupportCoinSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        SupportCoin = self.get_object(pk)
        serializer = SupportCoinSerializer(SupportCoin, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SupportCoinStatisticList(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    serializer_class = SupportCoinSerializer

    def get_queryset(self):
        """
            This view should return a list of all the purchases for
            the user as determined by the username portion of the URL.
            """
        busker = self.kwargs['busker']
        start_date = self.kwargs['start_date']
        end_date = self.kwargs['end_date']

        queryset = supportCoin.objects.filter(busker=busker, date_created__gte=start_date, date_created__lte=end_date).values('coin_amount', 'date_created').annotate(
            follower_count=Count('coin_amount')).order_by('date_created')

        return queryset.distinct();

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        return Response(queryset)

class RoadConcertView(generics.CreateAPIView):
    queryset = RoadConcert.objects.all()
    serializer_class = RoadConcertSerializer

    def get_object(self, pk):
        try:
            return RoadConcert.objects.get(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = RoadConcertSerializer(event)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = RoadConcertSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        RoadConcert = self.get_object(pk)
        serializer = SupportCoinSerializer(RoadConcert, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#실시간 버스킹
class LiveRoadConcertView(generics.ListAPIView):
   serializer_class = RoadConcertSerializer

   def get_queryset(self):
       """
       This view should return a list of all the purchases for
       the user as determined by the username portion of the URL.
       """
       road_concert_date = self.kwargs['road_concert_date']
       current_time = self.kwargs['current_time']

       return RoadConcert.objects.filter(road_concert_date=road_concert_date, road_concert_start_time__lte=current_time, road_concert_end_time__gte=current_time)

#예약된거 보기
class ReservationRoadConcert(generics.ListAPIView):
   serializer_class = RoadConcertSerializer
   def get_queryset(self):
       """
       This view should return a list of all the purchases for
       the user as determined by the username portion of the URL.
       """
       road_address = self.kwargs['road_address']
       road_concert_date = self.kwargs['road_concert_date']

       return RoadConcert.objects.filter(road_address=road_address, road_concert_date=road_concert_date)
