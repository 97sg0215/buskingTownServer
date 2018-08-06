from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from busking.models import BuskerRank
from busking.serializers import BuskerRankSerializer


class BuskerRank(viewsets.ModelViewSet):
    queryset = BuskerRank.objects.all()
    serializer_class = BuskerRankSerializer