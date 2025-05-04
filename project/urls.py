from django.contrib import admin

from django.urls import path, include
from mainapp.views import *  # Import views from main app
from userauth.views import *  # Import views from userauth app, including logout_view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns  # Static files serving

urlpatterns = [
      # =====================
    # HTML PAGE ROUTES
    # =====================
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('contact/', contact_view, name='contact'),
    path('tickets/', tickets_view, name='tickets'),
    path('cart/', cart_view, name='cart_view'),
    path('logout/', logout_view, name='logout'),
    

    path('', include('hotel.urls')),  # Include hotel app URLs


      
    

    
    # Cart actions (HTML forms)
    path('cart/add/', add_to_cart_view, name='add_to_cart'),
  path('cart/delete/', delete_cart, name='delete_cart'),

    # =====================
    # API JSON ENDPOINTS
    # =====================
    path('api/tickets/', api_tickets, name='api_tickets'),
    path('api/cart/',api_cart, name='api_cart'),
    path('api/cart/add/', api_add_to_cart, name='api_add_to_cart'),
    path('api/cart/clear/', api_delete_cart, name='api_delete_cart'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)