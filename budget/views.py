import json
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Projet, Poste, LigneDesignation


# ── Pages HTML ─────────────────────────────────────────────────

def dashboard(request):
    projets = Projet.objects.all().order_by('-date_creation')
    return render(request, 'budget/dashboard.html', {'projets': projets})


def projet_detail(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    return render(request, 'budget/projet_detail.html', {'projet': projet})


# ── API Projets ────────────────────────────────────────────────

@csrf_exempt
def api_projets(request):
    if request.method == 'GET':
        data = [{'id': p.id, 'nom': p.nom, 'budget_avance': str(p.budget_avance)}
                for p in Projet.objects.all()]
        return JsonResponse(data, safe=False)

    if request.method == 'POST':
        body = json.loads(request.body)
        p = Projet.objects.create(
            nom=body['nom'],
            budget_avance=body.get('budget_avance', 0)
        )
        return JsonResponse({'id': p.id, 'nom': p.nom}, status=201)


@csrf_exempt
def api_projet_detail(request, pk):
    projet = get_object_or_404(Projet, pk=pk)

    if request.method == 'PATCH':
        body = json.loads(request.body)
        for field in ['nom', 'budget_avance']:
            if field in body:
                setattr(projet, field, body[field])
        projet.save()
        return JsonResponse({'id': projet.id, 'nom': projet.nom})

    if request.method == 'DELETE':
        projet.delete()
        return JsonResponse({'deleted': True})


# ── API Postes ─────────────────────────────────────────────────

@csrf_exempt
def api_postes(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        poste = Poste.objects.create(
            projet_id=body['projet_id'],
            nom=body['nom'],
            ordre=body.get('ordre', 0)
        )
        return JsonResponse({'id': poste.id, 'nom': poste.nom}, status=201)


@csrf_exempt
def api_poste_detail(request, pk):
    poste = get_object_or_404(Poste, pk=pk)

    if request.method == 'PATCH':
        body = json.loads(request.body)
        if 'nom' in body:
            poste.nom = body['nom']
        poste.save()
        return JsonResponse({'id': poste.id, 'nom': poste.nom})

    if request.method == 'DELETE':
        poste.delete()
        return JsonResponse({'deleted': True})


# ── API Lignes ─────────────────────────────────────────────────

@csrf_exempt
def api_lignes(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        devis_val = float(body.get('devis', 0) or 0)
        devis_revu_val = body.get('devis_revu', '')
        ligne = LigneDesignation.objects.create(
            poste_id=body['poste_id'],
            designation=body['designation'],
            devis=devis_val,
            devis_revu=float(devis_revu_val) if devis_revu_val not in ('', None, '0', 0) else devis_val,
            avance=float(body.get('avance', 0) or 0),
        )
        return JsonResponse({
            'id': ligne.id,
            'designation': ligne.designation,
            'devis': str(ligne.devis),
            'devis_revu': str(ligne.devis_revu),
            'avance': str(ligne.avance),
            'reliquat': str(ligne.reliquat()),
        }, status=201)


@csrf_exempt
def api_ligne_detail(request, pk):
    ligne = get_object_or_404(LigneDesignation, pk=pk)

    if request.method == 'PATCH':
        body = json.loads(request.body)
        for field in ['designation', 'devis', 'devis_revu', 'avance']:
            if field in body:
                if field != 'designation':
                   setattr(ligne, field, float(body[field]) if body[field] not in ('', None) else 0)  
                else:
                    setattr(ligne, field, body[field])
        ligne.save()
        return JsonResponse({
            'id': ligne.id,
            'designation': ligne.designation,
            'devis': str(ligne.devis),
            'devis_revu': str(ligne.devis_revu),
            'avance': str(ligne.avance),
            'reliquat': str(ligne.reliquat()),
        })

    if request.method == 'DELETE':
        ligne.delete()
        return JsonResponse({'deleted': True})


# ── API Récap ──────────────────────────────────────────────────

def api_recap(request, pk):
    projet = get_object_or_404(Projet, pk=pk)
    return JsonResponse({
        'budget_avance':    str(projet.budget_avance),
        'budget_estimatif': str(projet.budget_estimatif()),
        'imprevu':          str(projet.imprevu()),
        'total_avances':    str(projet.total_avances()),
        'en_caisse':        str(projet.en_caisse()),
        'reliquat_def':     str(projet.reliquat_def()),
        'surplus':          str(projet.surplus()),
    })