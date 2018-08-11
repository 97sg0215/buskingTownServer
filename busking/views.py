from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from busking.models import TopBusker
from busking.serializers import BuskerRankSerializer

#버스커 랭킹 뷰
class BuskerRank(viewsets.ModelViewSet):
    queryset = TopBusker.objects.all()
    serializer_class = BuskerRankSerializer