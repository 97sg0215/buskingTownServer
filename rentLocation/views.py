from datetime import timedelta

from django.http import Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.utils import timezone
from rest_framework import generics, status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from rentLocation import models
from rentLocation.models import Provide, ProvideOption, ReservationPracticeRoom
from rentLocation.serializers import ProvideSerializer, ProvideOptionSerializer, ReservationPracticeRoomSerializer

from django.db.models import Sum, F, Q



class ProvideAllList(viewsets.ModelViewSet):
    queryset = Provide.objects.all()
    serializer_class = ProvideSerializer

class ProvideUserView(APIView):
    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        provides = event.get_provides()
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


#버스커가 대여시 보는 화면
class PracticeRoomList(viewsets.ModelViewSet):
    #제공하는 날짜와 시간
    available_start_date = Provide.objects.values('provide_start_date')
    available_end_date = Provide.objects.values('provide_end_date')

    #오늘 날짜
    today_date = timezone.now().date()

    queryset = Provide.objects.filter(provide_type=1).exclude(provide_end_date__lte=timezone.now().date()).prefetch_related('reservation_provide')
    serializer_class = ProvideSerializer


class ConcertRoomList(viewsets.ModelViewSet):
    queryset = Provide.objects.filter(provide_type=2)
    serializer_class = ProvideSerializer


#예약된거 보기
class ReservationPractice(generics.ListAPIView):
   serializer_class = ReservationPracticeRoomSerializer

   def get_queryset(self):
       """
       This view should return a list of all the purchases for
       the user as determined by the username portion of the URL.
       """
       provide = self.kwargs['provide']
       provide_option = self.kwargs['provide_option']
       practice_date = self.kwargs['practice_date']

       return ReservationPracticeRoom.objects.filter(provide=provide, provide_option=provide_option, practice_date=practice_date)

class Reservation(APIView):
    def get_object(self, pk):
        try:
            return ReservationPracticeRoom.objects.get(pk=pk)
        except ReservationPracticeRoom.DoesNotExist:
            raise Http404

    def get(self, request, pk,format=None):
        event = self.get_object(pk)
        serializer = ReservationPracticeRoomSerializer(event)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer_class = ReservationPracticeRoomSerializer(data=request.data)
        if serializer_class.is_valid():
            serializer_class.save()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = ReservationPracticeRoomSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)