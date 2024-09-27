from django.urls import path
from .views import landing, about, contact

urlpatterns = [
    path('', landing, name='landing'),  # Landing page
    path('about/', about, name='about'),  # About page
    path('contact/', contact, name='contact'),  # Contact page
    
]

from django.conf.urls import handler404, handler500
from .views import handler404, handler500

handler404 = 'global.views.handler404'  # Replace 'yourapp' with your app name
handler500 = 'global.views.handler500'
