from rest_framework import serializers
from .models import Room, Reservation

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ['id', 'number', 'room_type', 'price_per_night', 'location', 'image']

class ReservationSerializer(serializers.ModelSerializer):
    room_number = serializers.CharField(source='room.number', read_only=True)
    room_type = serializers.CharField(source='room.room_type', read_only=True)
    location = serializers.CharField(source='room.location', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Reservation
        fields = ['id', 'room_number', 'room_type', 'location', 'start_date', 'end_date', 'total_price']

    def get_total_price(self, obj):
        nights = (obj.end_date - obj.start_date).days
        return float(obj.room.price_per_night * nights)
