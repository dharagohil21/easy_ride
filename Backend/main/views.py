from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from main.serializers import UserSerializer, RideSerializer
from main.models import AppUser, Ride
from django.db import IntegrityError
from uuid import uuid4
from django.db.models import Q


def authorize_access_token(at):

    try:

        user = AppUser.objects.get(access_token=at)

    except AppUser.DoesNotExist :

        return False

    return user

@api_view(['POST'])
def register(request):
    
    keys = request.POST.keys()

    if(not("email" in keys and "first_name" in keys and "last_name" in keys and "phone_number" in keys and "password" in keys)):

        return Response(data={"error": "Invalid form data."}, status=status.HTTP_400_BAD_REQUEST)

    else:

        user = AppUser()
        user.first_name = request.POST["first_name"]
        user.last_name = request.POST["last_name"]
        user.email = request.POST["email"]
        user.phone_number = request.POST["phone_number"]
        user.password = request.POST["password"]

        try:

            user.save()

        except IntegrityError:

            return Response(data={"error" : "User already exists."}, status=status.HTTP_409_CONFLICT)

        serrialized = UserSerializer(user, many=False)
        return Response(serrialized.data)


@api_view(['POST'])
def login(request):
    
    keys = request.POST.keys()

    if(not("email" in keys and "password" in keys)):

        return Response(data={"error": "Invalid form data."}, status=status.HTTP_400_BAD_REQUEST)

    else:
        
        try:

            user = AppUser.objects.get(email=request.POST["email"])
            
            if(user.password == request.POST["password"]):

                user.access_token = uuid4()
                user.save()

                serrialized = UserSerializer(user, many=False)
                return Response(serrialized.data)

            else:

                return Response(data={"error": "User not found or password incorrect."}, status=status.HTTP_401_UNAUTHORIZED)

        except AppUser.DoesNotExist :

            return Response(data={"error": "User not found or password incorrect."}, status=status.HTTP_401_UNAUTHORIZED)
            
@api_view(['GET', 'POST', 'DELETE', 'PATCH'])
def rides(request):

    if (request.method == 'GET'):

        keys = request.GET.keys()

        if(not("access_token" in keys)):

            return Response(data={"error": "Invalid form data."}, status=status.HTTP_400_BAD_REQUEST)

        else:

            user = authorize_access_token(request.GET["access_token"])

            if not user:

                return Response(data={"error": "Invalid access token."}, status=status.HTTP_401_UNAUTHORIZED)

            if ("query" in request.GET.keys()):

                rides = Ride.objects.filter(Q(ride_title__icontains=request.GET["query"]) | Q(origin__icontains=request.GET["query"]) | Q(destination__icontains=request.GET["query"]))

            else:

                rides = Ride.objects.all()

            serrialized = RideSerializer(rides, many=True)

            return Response(serrialized.data)
    
    elif (request.method == 'POST'):

        keys = request.POST.keys()

        if(not("access_token" in keys and "ride_title" in keys and "origin" in keys and "destination" in keys and "time" in keys and "price" in keys)):

            return Response(data={"error": "Invalid form data."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            
            user = authorize_access_token(request.POST["access_token"])

            if not user:

                return Response(data={"error": "Invalid access token."}, status=status.HTTP_401_UNAUTHORIZED)

            ride = Ride()
            ride.ride_title = request.POST["ride_title"]
            ride.origin = request.POST["origin"]
            ride.destination = request.POST["destination"]
            ride.time = request.POST["time"]
            ride.price = request.POST["price"]
            ride.save()

            user.rides.add(ride)

            user.save()

            serrialized = RideSerializer(ride, many=False)
            return Response(serrialized.data)

    if (request.method == 'DELETE'):

        keys = request.GET.keys()

        if(not("access_token" in keys and "ride_id" in keys)):

            return Response(data={"error": "Invalid form data."}, status=status.HTTP_400_BAD_REQUEST)

        else:
            
            user = authorize_access_token(request.GET["access_token"])

            if not user:

                return Response(data={"error": "Invalid access token."}, status=status.HTTP_401_UNAUTHORIZED)
            
            try:
                
                ride = user.rides.get(id=request.GET["ride_id"])
            
            except Ride.DoesNotExist:

                return Response(data={"error": "Ride does not exist or you do not own it."}, status=status.HTTP_400_BAD_REQUEST)

            ride.delete()

            return Response(data={"message": "Ride deleted."})

    if request.method == "PATCH":

        keys = request.GET.keys()

        if(not("access_token" in keys and "ride_id" in keys)):

            return Response(data={"error": "Invalid form data."}, status=status.HTTP_400_BAD_REQUEST)

            
        user = authorize_access_token(request.GET["access_token"])

        if not user:

                return Response(data={"error": "Invalid access token."}, status=status.HTTP_401_UNAUTHORIZED)

        try:
                
            ride = user.rides.get(id=request.GET["ride_id"])
            
        except Ride.DoesNotExist:

            return Response(data={"error": "Ride does not exist or you do not own it."}, status=status.HTTP_400_BAD_REQUEST)


        valid_keys = ['ride_title', 'origin', 'destination', 'time', 'price']

        for key in request.GET.keys():

            if key != "access_token" and key in valid_keys:

                setattr(ride, key, request.GET[key])

        try:

            ride.save()

        except Exception as e:

            return Response(data={"error": "Update failed, atleast one of the parameters was incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        serrialized = RideSerializer(ride, many=False)
        return Response(serrialized.data)

@api_view(['GET', 'PATCH', 'DELETE'])
def account(request):

    keys = request.GET.keys()

    if(not("access_token" in keys)):

        return Response(data={"error": "Invalid form data."}, status=status.HTTP_400_BAD_REQUEST)

    user = authorize_access_token(request.GET["access_token"])

    if not user:

                return Response(data={"error": "Invalid access token."}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == "PATCH":

        valid_keys = ['first_name', 'last_name', 'email', 'password', 'phone_number']

        for key in request.GET.keys():

            print(key in valid_keys)

            if key != "access_token" and key in valid_keys:

                setattr(user, key, request.GET[key])

        try:

            user.save()

        except Exception as e:

            return Response(data={"error": "Update failed, atleast one of the parameters was incorrect."}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":

        user.delete()

        return Response(data={"message": "User account deleted."})

    serrialized = UserSerializer(user, many=False)
    return Response(serrialized.data)