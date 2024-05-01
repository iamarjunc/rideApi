
from django.shortcuts import render

from .models import CustomUser, Ride
from .serializers import UserSerializer, LoginSerializer, RideSerializer, StatusUpdateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import status

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = CustomUser.objects.filter(username=username).first()
            if user and user.check_password(password):
                return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Invalid username or password'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateRideView(APIView):
    def post(self, request):
        serializer = RideSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RideDetailView(APIView):
    def get(self, request, ride_id):
        ride = Ride.objects.filter(id=ride_id).first()
        if ride:
            serializer = RideSerializer(ride)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

class ListRidesView(APIView):
    def get(self, request):
        rides = Ride.objects.all()
        serializer = RideSerializer(rides, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RideStatusUpdateView(APIView):
    def patch(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
            new_status = request.data.get('status')
            if new_status in dict(Ride.STATUS_CHOICES):
                ride.status = new_status
                ride.save()
                return Response({'message': 'Ride status updated successfully'})
            return Response({'message': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        except Ride.DoesNotExist:
            return Response({'message': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

class RideCurrentLocationUpdateView(APIView):
    def patch(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
            current_location = request.data.get('current_location')
            ride.current_location = current_location
            ride.save()
            return Response({'message': 'Ride current location updated successfully'})
        except Ride.DoesNotExist:
            return Response({'message': 'Ride not found'}, status=status.HTTP_404_NOT_FOUND)

class RideAcceptView(APIView):
    def post(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
            if ride.status == 'PENDING':
                ride.status = 'ACCEPTED'
                ride.save()
                return Response({'message': 'Ride request accepted successfully'})
            else:
                return Response({'message': 'Ride request is not pending'}, status=status.HTTP_400_BAD_REQUEST)
        except Ride.DoesNotExist:
            return Response({'message': 'Ride request not found'}, status=status.HTTP_404_NOT_FOUND)
