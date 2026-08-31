# Immovia

Application Django de gestion immobilière et de suivi de projets.

## Prérequis

- Python 3.11+
- pip
- virtualenv / venv

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Tests

```bash
python manage.py test
```

## Déploiement

Le projet est prêt pour le déploiement Django standard avec un serveur web compatible WSGI/ASGI.
