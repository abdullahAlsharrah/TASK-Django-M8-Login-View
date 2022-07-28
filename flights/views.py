import datetime

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from flights import serializers
from flights.models import Booking, Flight
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser


class FlightsList(generics.ListAPIView):
    queryset = Flight.objects.all()
    serializer_class = serializers.FlightSerializer


class BookingsList(generics.ListAPIView):
    serializer_class = serializers.BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(date__gte=datetime.date.today())


class BookingDetails(generics.RetrieveAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.BookingDetailsSerializer
    lookup_url_kwarg = "booking_id"

class FlightDetail(generics.RetrieveAPIView):
    queryset = Flight.objects.all()
    serializer_class = serializers.FlightSerializer
    lookup_url_kwarg = "flight_id"

class CreateBooking(generics.RetrieveAPIView,generics.CreateAPIView):
    serializer_class = serializers.UpdateBookingSerializer
    permission_class=[IsAuthenticated,]
    def perform_create(self, serializer):
        params=self.request.GET
        flight_id =params.get('flight_id')
        flight = Flight.objects.get(id=flight_id)
        serializer.save(user = self.request.user, flight=flight)
        
    

class UpdateBooking(generics.RetrieveUpdateAPIView):
    queryset = Booking.objects.all()
    serializer_class = serializers.UpdateBookingSerializer
    lookup_url_kwarg = "booking_id"


class CancelBooking(generics.DestroyAPIView):
    queryset = Booking.objects.all()
    lookup_url_kwarg = "booking_id"

class UserLogInApiView(APIView):
    serializer_class= serializers.UserLogInSerilizer
    def post(self, request):
        data= request.data
        serializer = serializers.UserLogInSerilizer(data=data)
        if serializer.is_valid(raise_exception=True):
            valid_data = serializer.data
            return Response(valid_data, status=HTTP_200_OK)
        return Response(serializer.error,HTTP_400_BAD_REQUEST)

# trying to add more details in the token by using this class 
class UserTokenApiView(TokenObtainPairView):
    serializer_class= serializers.UserTokenSerializer
 

