from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import generics
from rest_framework import filters as restframework_filters

from django_filters import AllValuesFilter, DateTimeFilter, NumberFilter

from drones.models import DroneCategory
from drones.models import Drone
from drones.models import Pilot
from drones.models import Competition

from drones.serializers import DroneCategorySerializer
from drones.serializers import DroneSerializer
from drones.serializers import PilotSerializer
from drones.serializers import PilotCompetitionSerializer


class DroneCategoryList(generics.ListCreateAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-list'

    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class DroneCategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = DroneCategory.objects.all()
    serializer_class = DroneCategorySerializer
    name = 'dronecategory-detail'

    filter_fields = ('name',)
    search_fields = ('^name',)
    ordering_fields = ('name',)


class DroneList(generics.ListCreateAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-list'

    filter_fields = ('name',
                     'drone_category',
                     'manufacturing_date',
                     'has_it_completed',)
    search_fields = ('^name',)
    ordering_fields = ('name',
                       'manufacturing_date',)


class DroneDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Drone.objects.all()
    serializer_class = DroneSerializer
    name = 'drone-detail'


class PilotList(generics.ListCreateAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-list'

    filter_fields = ('name',
                     'gender',
                     'races_count')
    search_fields = ('^name',)
    ordering_fields = ('name',
                       'races_count')


class PilotDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pilot.objects.all()
    serializer_class = PilotSerializer
    name = 'pilot-detail'


class CompetitionFilter(restframework_filters.FilterSet):
    from_achievement_date = DateTimeFilter(label='Distance achievement date starts from',
                                           name='distance_achievement_date',
                                           lookup_expr='gte')
    to_achievement_date = DateTimeFilter(label='Distance achievement date ends with',
                                         name='distance_achievement_date',
                                         lookup_expr='lte')
    min_distance_in_feet = NumberFilter(label='Distance in feet large than',
                                        name='distance_in_feet',
                                        lookup_expr='gte')
    max_distance_in_feet = NumberFilter(label='Distance in feet less than',
                                        name='distance_in_feet',
                                        lookup_expr='lte')
    drone_name = AllValuesFilter(label='✈️ Drone‍', name='drone__name')
    pilot_name = AllValuesFilter(label='👩 Pilot', name='pilot__name')

    class Meta:
        model = Competition
        fields = ('distance_in_feet',
                  'from_achievement_date',
                  'to_achievement_date',
                  'min_distance_in_feet',
                  'max_distance_in_feet',
                  'drone_name',  # drone__name => drone_name
                  'pilot_name')  # pilot__name => pilot_name


class CompetitionList(generics.ListCreateAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-list'

    filter_class = CompetitionFilter
    ordering_fields = ('distance_in_feet',
                       'distance_achievement_date',)


class CompetitionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Competition.objects.all()
    serializer_class = PilotCompetitionSerializer
    name = 'competition-detail'


class APIRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):
        return Response({
            'drone-categories': reverse(DroneCategoryList.name, request=request),
            'drones'          : reverse(DroneList.name, request=request),
            'pilots'          : reverse(PilotList.name, request=request),
            'competitions'    : reverse(CompetitionList.name, request=request),
        })
