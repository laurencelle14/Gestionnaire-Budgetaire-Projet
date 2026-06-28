# Gestionnaire Budgétaire de Projet

Application web de suivi budgétaire de chantier, développée avec Django, PostgreSQL et JavaScript vanilla.

## Fonctionnalités

- Création et gestion de projets budgétaires
- Ajout de postes par projet (Peinture, Plomberie, Maçonnerie...)
- Saisie de lignes de désignation avec Devis, Devis révu, Avance
- Calcul automatique en temps réel :
  - Reliquat = Devis révu - Avance
  - Budget estimatif travaux = Σ Devis révu
  - Imprévus (10%)
  - En caisse = Budget avancé - Total avances
  - Reliquat définitif
  - Surplus
- Interface responsive, installable sur mobile (PWA)
- Modals de confirmation pour les suppressions

## Stack technique

- **Backend** : Django 5.0 + Python 3.12
- **Base de données** : PostgreSQL
- **Frontend** : HTML / CSS / JavaScript vanilla
- **Déploiement** : Railway
- **Serveur** : Gunicorn + Whitenoise

## Installation locale

### Prérequis

- Python 3.12
- PostgreSQL

### Étapes

```bash
# Cloner le repo
git clone https://github.com/laurencelle14/budget-chantier.git
cd budget-chantier

# Créer et activer l'environnement virtuel
python -m venv env
env\Scripts\activate  # Windows
source env/bin/activate  # Mac/Linux

# Installer les dépendances
pip install -r requirements.txt

# Créer le fichier .env
cp .env.example .env
# Remplir les variables dans .env

# Créer la base de données PostgreSQL
createdb budget_chantier

# Lancer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Lancer le serveur
python manage.py runserver
```

## Variables d'environnement

Créer un fichier `.env` à la racine du projet :

```
SECRET_KEY=votre-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=budget_chantier
DB_USER=postgres
DB_PASSWORD=votre-mot-de-passe
DB_HOST=localhost
DB_PORT=5432
```

## Déploiement sur Railway

1. Pusher le code sur GitHub
2. Créer un nouveau projet sur [Railway](https://railway.app)
3. Connecter le repo GitHub
4. Ajouter un service PostgreSQL
5. Configurer les variables d'environnement :
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=votre-domaine.railway.app`
   - `DATABASE_URL` (injecté automatiquement par Railway)
6. Lancer les migrations via la Console Railway :
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

## Structure du projet

```
budget-chantier/
├── budget/                  # App principale
│   ├── models.py            # Projet, Poste, LigneDesignation
│   ├── views.py             # Vues HTML + API JSON
│   ├── urls.py
│   └── admin.py
├── budget_chantier/         # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
│   └── budget/
│       ├── base.html
│       ├── dashboard.html
│       └── projet_detail.html
├── static/                  # Fichiers statiques (PWA)
├── manage.py
├── requirements.txt
├── Procfile
└── runtime.txt
```

## Modèles de données

```
Projet
├── nom
├── budget_avance
└── taux_imprevu (10%)

Poste
├── projet (FK)
├── nom
└── ordre

LigneDesignation
├── poste (FK)
├── designation
├── devis
├── devis_revu
└── avance
```

## Installation PWA sur iPhone

1. Ouvrir Safari sur l'iPhone
2. Naviguer vers l'URL de l'application
3. Appuyer sur le bouton **Partager**
4. Sélectionner **Sur l'écran d'accueil**
5. Appuyer sur **Ajouter**

## Auteur

Développé par **Armel**