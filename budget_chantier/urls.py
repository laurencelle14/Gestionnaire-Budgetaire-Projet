from django.contrib import admin
from django.urls import path, include
from budget import views_auth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('budget.urls')),
]