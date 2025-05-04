from django import forms
from .models import Reservation
from .models import Rating

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['start_date', 'end_date']

