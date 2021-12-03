from rest_framework import serializers
from main.models import AppUser, Ride

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = AppUser
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'access_token']

class RideSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Ride
        fields = ['id', 'ride_title', 'origin', 'destination', 'time', 'price', 'created']

