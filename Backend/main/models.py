from django.db import models
import uuid

class Ride(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ride_title = models.CharField(max_length=128)
    
    origin = models.CharField(max_length=128)
    destination = models.CharField(max_length=10)

    time = models.CharField(max_length=128)

    price = models.DecimalField(decimal_places=2, max_digits=10)

    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

class AppUser(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email= models.EmailField(unique=True)

    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=10)

    password = models.CharField(max_length=128)

    access_token = models.UUIDField(default=uuid.uuid4)

    rides = models.ManyToManyField('Ride')

    created = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)


    