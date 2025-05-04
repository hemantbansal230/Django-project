from django.db import models
from django.contrib.auth.models import User  # Use Django's built-in User model

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()

    def __str__(self):
        return self.name

class Ticket(models.Model):
    event_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.event_name

class Cart(models.Model): 
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Prevent negative or zero quantity
    
    def __str__(self):
        return f'{self.user.username} - {self.ticket.event_name}'

    @property
    def total_price(self):
        """Calculate total price for the cart item"""
        return self.quantity * self.ticket.price
