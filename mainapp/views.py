from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Ticket, Contact, Cart
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import TicketSerializer, CartItemSerializer

# ======================
# HTML VIEWS (FOR PAGES)
# ======================

def home(request):
    events = Ticket.objects.all()
    return render(request, 'main.html', {'events': events})

def contact_view(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        Contact.objects.create(name=name, email=email, message=message)
        messages.success(request, "Thanks for contacting us!")
        return redirect('contact')
    return render(request, 'contact.html')

def tickets_view(request):
    tickets = Ticket.objects.all()
    return render(request, 'tickets.html', {'tickets': tickets})

@login_required
def add_to_cart_view(request):
    if request.method == 'POST':
        ticket_id = request.POST['ticket_id']
        quantity = int(request.POST['quantity'])
        ticket = Ticket.objects.get(id=ticket_id)

        cart_item, created = Cart.objects.get_or_create(user=request.user, ticket=ticket)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        messages.success(request, "Added to cart!")
        return redirect('tickets')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('ticket')
    total = sum(item.quantity * item.ticket.price for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total': total
    })


@login_required
def delete_cart(request):
    if request.method == 'POST':
        Cart.objects.filter(user=request.user).delete()
        messages.success(request, 'Cart has been emptied!')
    return redirect('/cart/')


def logout_view(request):
    logout(request)
    return redirect('home')

# ======================
# API VIEWS (JSON ONLY)
# ======================

@api_view(['GET'])
def api_tickets(request):
    tickets = Ticket.objects.all()
    serializer = TicketSerializer(tickets, many=True)
    return Response({
        'status': 'success',
        'tickets': serializer.data
    })

# ---------------------
# API: Add to cart
# ---------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def api_add_to_cart(request):
    try:
        ticket_id = request.data.get('ticket_id')
        quantity = int(request.data.get('quantity', 1))

        ticket = Ticket.objects.get(id=ticket_id)
        cart_item, created = Cart.objects.get_or_create(
            user=request.user,
            ticket=ticket,
            defaults={'quantity': quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartItemSerializer(cart_item)
        return Response({
            'status': 'success',
            'message': 'Item added to cart',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)

    except Ticket.DoesNotExist:
        return Response({'status': 'error', 'message': 'Ticket not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# ---------------------
# API: View cart
# ---------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def api_cart(request):
    cart_items = Cart.objects.filter(user=request.user).select_related('ticket')
    serializer = CartItemSerializer(cart_items, many=True)
    total = sum(item.quantity * item.ticket.price for item in cart_items)

    return Response({
        'status': 'success',
        'cart_items': serializer.data,
        'cart_total': float(total)
    })

# ---------------------
# API: Clear cart
# ---------------------
@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def api_delete_cart(request):
    try:
        deleted_count, _ = Cart.objects.filter(user=request.user).delete()
        return Response({
            'status': 'success',
            'message': 'Cart cleared',
            'items_deleted': deleted_count
        })
    except Exception as e:
        return Response({
            'status': 'error',
            'message': str(e)
        }, status=status.HTTP_400_BAD_REQUEST)