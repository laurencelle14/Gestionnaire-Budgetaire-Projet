from django.contrib import admin
from .models import Projet, Poste, LigneDesignation


class LigneInline(admin.TabularInline):
    model = LigneDesignation
    extra = 1


class PosteInline(admin.StackedInline):
    model = Poste
    extra = 1


@admin.register(Projet)
class ProjetAdmin(admin.ModelAdmin):
    list_display = ['nom', 'budget_avance', 'date_creation']
    inlines = [PosteInline]


@admin.register(Poste)
class PosteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'projet']
    inlines = [LigneInline]


@admin.register(LigneDesignation)
class LigneAdmin(admin.ModelAdmin):
    list_display = ['designation', 'poste', 'devis', 'devis_revu', 'avance']