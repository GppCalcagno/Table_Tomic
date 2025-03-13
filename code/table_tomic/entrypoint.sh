#!/bin/sh


# Applica le migrazioni
echo "Eseguo makemigrations..."
python manage.py makemigrations --noinput

echo "Eseguo migrate..."
python manage.py migrate

# Crea il superuser solo se non esiste
echo "Creo il superuser se non esiste..."
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser("admin", "admin@admin.com", "admin")
    print("Superuser creato!")
else:
    print("Superuser già esistente, nessuna azione necessaria.")
EOF

# Avvia Gunicorn per servire Django
echo "Avvio Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 table_tomic.wsgi:application