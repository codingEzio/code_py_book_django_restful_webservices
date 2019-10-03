from rest_framework import serializers

from drones import views
from drones.models import (
    Drone,
    DroneCategory,
    Pilot,
    Competition,
)


class DroneCategorySerializer(serializers.HyperlinkedModelSerializer):
    drones = serializers.HyperlinkedModelSerializer(many=True,
                                                    read_only=True,
                                                    view_name='drone-detail')
