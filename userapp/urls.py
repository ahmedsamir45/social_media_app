from django.urls import path
from .views import register_view, dashboard, LoginView,logout_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),  
    path('register/', register_view, name='register'),
    path('dashboard/', dashboard, name='dashboard'),
      path('logout/', logout_view, name='logout'),  # Logout path
]
