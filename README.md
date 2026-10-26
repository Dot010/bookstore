# Bookstore API

API de livraria feita com Django e Django REST Framework.

## Como rodar
1. Instale o Poetry
2. Copie o `.env.example` para `.env` e preencha a `SECRET_KEY`
3. `poetry install`
4. `poetry run python manage.py migrate`
5. `poetry run python manage.py runserver`

## Gerando uma SECRET_KEY
```
poetry run python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```