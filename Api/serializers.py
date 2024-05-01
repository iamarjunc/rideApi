
from rest_framework import serializers
from .models import CustomUser
from .models import Ride

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            
        )
        return user

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password')


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()




class RideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ride
        fields = '__all__'

class StatusUpdateSerializer(serializers.Serializer):
    status = serializers.CharField()