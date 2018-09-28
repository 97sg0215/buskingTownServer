from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from rentLocation.models import Provide, ProvideOption
from rentLocation.serializers import ProvideSerializer, ProvideOptionSerializer

class ProvideAllList(viewsets.ModelViewSet):
    queryset = Provide.objects.all()
    serializer_class = ProvideSerializer

class ProvideUserView(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        provides = event.get_options()
        serializer = ProvideSerializer(provides, many=True)
        return Response(serializer.data)

class ProvideView(generics.CreateAPIView):
    queryset = Provide.objects.all()
    serializer_class = ProvideSerializer
    parser_classes = (MultiPartParser,)

    def get_object(self, pk):
        try:
            return Provide.objects.get(pk=pk)
        except Provide.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = ProvideSerializer(event)
        return Response(serializer.data)


    def post(self, request, *args, **kwargs):
        serializer_class = ProvideSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        Provide = self.get_object(pk)
        serializer = ProvideSerializer(Provide, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class ProvideOptionList(APIView):
    def get_object(self, pk):
        try:
            return Provide.objects.get(pk=pk)
        except Provide.DoesNotExist:
            raise Http404

    def get(self, request, pk,format=None):
        event = self.get_object(pk)
        options = event.get_options()
        serializer = ProvideOptionSerializer(options, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = ProvideOptionSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        options = event.get_options()
        serializer = ProvideOptionSerializer(options, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)