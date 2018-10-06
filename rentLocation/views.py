from django.http import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import generics, status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from rentLocation.models import Provide, ProvideOption, ReservationPracticeRoom
from rentLocation.serializers import ProvideSerializer, ProvideOptionSerializer, ReservationPracticeRoomSerializer


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
    queryset = Provide.objects.filter(provide_type="1")
    serializer_class = ProvideSerializer

class ConcertRoomList(viewsets.ModelViewSet):
    queryset = Provide.objects.filter(provide_type="2")
    serializer_class = ProvideSerializer

# #버스커가 예약할때
# class ReservationPracticeRoom_ex(generics.CreateAPIView):
#     queryset = ReservationPracticeRoom.objects.valuse('practice_date')
#     serializer_class = ReservationPracticeRoomSerializer


class ReservationPracticeRoom(APIView):
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

        #나를 제외한 다른 모델의 연습날짜 데이터
        # other_date = ReservationPracticeRoom.objects.values('practice_date').exclude(provide=self.provide)
        #
        # other_start_time = ReservationPracticeRoom.objects.values('practice_start_time').exclude(provide=self.provide)
        # other_end_time = ReservationPracticeRoom.objects.values('practice_end_time').exclude(provide=self.provide)
        #
        # other_time = ReservationPracticeRoom.objects.filter(
        #     practice_start_time__range=(other_start_time, other_end_time))
        #
        # available_start_time = Provide.objects.values('provide_start_time')
        # available_end_time = Provide.objects.values('provide_end_time')
        #
        # available_time = ReservationPracticeRoom.objects.filter(
        #     practice_start_time__range=(available_start_time, available_end_time))
        #
        # this_date = ReservationPracticeRoom.objects.filter(provide=self.provide).values('practice_date')
        # this_time = ReservationPracticeRoom.objects.filter(provide=self.provide).values('practice_start_time')

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
