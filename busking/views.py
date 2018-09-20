from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView

from accounts.models import Busker
from busking.models import TopBusker
from busking.models import Post
from busking.serializers import PostSerializer
from busking.serializers import BuskerRankSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import viewsets, status

#버스커 랭킹 뷰
class BuskerRank(viewsets.ModelViewSet):
    queryset = TopBusker.objects.all()
    serializer_class = BuskerRankSerializer


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