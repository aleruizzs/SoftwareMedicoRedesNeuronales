from django.contrib.auth.models import User

def run():
    if not User.objects.filter(username="admin").exists():
        User.objects.create_superuser("admin", "admin@example.com", "admin123")
        print("✅ Superusuario creado: admin / admin123")
    else:
        print("ℹ️ El superusuario ya existía")
