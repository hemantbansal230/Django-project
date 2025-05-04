from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=100, default='Unknown')  # ✅ Add location
    image = models.ImageField(upload_to='room_images/', blank=True, null=True)  # ✅ Add image

    def __str__(self):
        return f"Room {self.number} ({self.room_type})"


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"Reservation for {self.user.username} in Room {self.room.number}"
