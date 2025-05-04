# hotel/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Reservation
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer, ReservationSerializer
# ======================
# HTML VIEWS (FOR PAGES)
# ======================

def room_list(request):
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'hotel/room_list.html', {'rooms': rooms})

@login_required
def make_reservation(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if not room.is_available:
        messages.error(request, 'This room is no longer available.')
        return redirect('hotel:room_list')
    
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            
            reservation = Reservation.objects.create(
                user=request.user,
                room=room,
                start_date=start_date,
                end_date=end_date
            )
            
            room.is_available = False
            room.save()
            messages.success(request, 'Reservation created successfully!')
            return redirect('hotel:my_reservations')
            
        except Exception as e:
            messages.error(request, f'Error creating reservation: {str(e)}')
    
    return render(request, 'hotel/make_reservation.html', {'room': room})

@login_required
def my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    return render(request, 'hotel/my_reservations.html', {'reservations': reservations})

@login_required
def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    room = reservation.room
    reservation.delete()
    room.is_available = True
    room.save()
    messages.success(request, 'Reservation canceled successfully.')
    return redirect('hotel:my_reservations')

# ======================
# API VIEWS (JSON ONLY)
# ======================

@api_view(['GET'])
def api_rooms(request):
    rooms = Room.objects.filter(is_available=True)
    serializer = RoomSerializer(rooms, many=True, context={'request': request})
    return Response({'status': 'success', 'rooms': serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_make_reservation(request):
    room_id = request.data.get('room_id')
    start_date = request.data.get('start_date')
    end_date = request.data.get('end_date')

    if not all([room_id, start_date, end_date]):
        return Response({'status': 'error', 'message': 'Missing required fields'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        room = Room.objects.get(id=room_id, is_available=True)
        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

        reservation = Reservation.objects.create(
            user=request.user,
            room=room,
            start_date=start_date_obj,
            end_date=end_date_obj
        )
        room.is_available = False
        room.save()

        serializer = ReservationSerializer(reservation)
        return Response({'status': 'success', 'message': 'Reservation created', 'data': serializer.data}, status=201)

    except Room.DoesNotExist:
        return Response({'status': 'error', 'message': 'Room not found or unavailable'}, status=404)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_my_reservations(request):
    reservations = Reservation.objects.filter(user=request.user).select_related('room')
    serializer = ReservationSerializer(reservations, many=True)
    return Response({'status': 'success', 'reservations': serializer.data})

@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def api_cancel_reservation(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id, user=request.user)
        room = reservation.room
        reservation.delete()
        room.is_available = True
        room.save()
        return Response({'status': 'success', 'message': 'Reservation canceled'})
    except Reservation.DoesNotExist:
        return Response({'status': 'error', 'message': 'Reservation not found or unauthorized'}, status=404)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=400)