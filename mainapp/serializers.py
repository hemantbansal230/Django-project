from rest_framework import serializers
from .models import Ticket, Cart

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'event_name', 'price']

class CartItemSerializer(serializers.ModelSerializer):
    event_name = serializers.CharField(source='ticket.event_name', read_only=True)
    unit_price = serializers.FloatField(source='ticket.price', read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['ticket_id', 'event_name', 'quantity', 'unit_price', 'total_price']

    def get_total_price(self, obj):
        return float(obj.quantity * obj.ticket.price)
