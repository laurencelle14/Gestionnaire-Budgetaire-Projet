from django.urls import path
from budget import views

urlpatterns = [
    # Pages HTML
    path('', views.dashboard, name='dashboard'),
    path('projet/<int:pk>/', views.projet_detail, name='projet_detail'),

    # API Projets
    path('api/projets/', views.api_projets, name='api_projets'),
    path('api/projets/<int:pk>/', views.api_projet_detail, name='api_projet_detail'),

    # API Postes
    path('api/postes/', views.api_postes, name='api_postes'),
    path('api/postes/<int:pk>/', views.api_poste_detail, name='api_poste_detail'),

    # API Lignes
    path('api/lignes/', views.api_lignes, name='api_lignes'),
    path('api/lignes/<int:pk>/', views.api_ligne_detail, name='api_ligne_detail'),

    # API Récap
    path('api/projet/<int:pk>/recap/', views.api_recap, name='api_recap'),
]