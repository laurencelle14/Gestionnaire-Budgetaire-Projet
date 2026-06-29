from django.contrib import admin
from django.urls import path, include
from budget import views_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('budget.urls')),
    path('login/', views_auth.login_view, name='login'),
    path('verify-otp/', views_auth.verify_otp_view, name='verify_otp'),
    path('logout/', views_auth.logout_view, name='logout'),
]