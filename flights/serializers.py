from django.forms import models
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Booking, Flight
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ["destination", "time", "price", "id"]


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "id","user"]


class BookingDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["flight", "date", "passengers", "id","user"]


class UpdateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["date", "passengers"]

class UserLogInSerilizer(serializers.Serializer):
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        access = models.CharField(read_only=True,allow_blank=True)
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Sorry, This user dosen't exist")
        
        if not user.check_password(password):
            raise serializers.ValidationError("Sorry, password is wrong")
        
        payload = RefreshToken.for_user(user)
        token = str(payload.access_token)
        data["access"] = token
        return data

## for adding more details such as username in the token
class UserTokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
        
