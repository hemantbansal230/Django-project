# hotel/urls.py
from django.urls import path
from . import views

app_name = 'hotel'

urlpatterns = [
    path('rooms/', views.room_list, name='room_list'),
    path('rooms/<int:room_id>/reserve/', views.make_reservation, name='make_reservation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
      # API routes
    path('api/rooms/', views.api_rooms, name='api_rooms'),
    path('api/reserve/', views.api_make_reservation, name='api_make_reservation'),
    path('api/my-reservations/', views.api_my_reservations, name='api_my_reservations'),
    path('api/cancel/<int:reservation_id>/', views.api_cancel_reservation, name='api_cancel_reservation'),
]
