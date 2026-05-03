"""
WSGI config for portal_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portal_project.settings')

application = get_wsgi_application()


# ─── Auto-create admin user on startup ────────────────────────────────────────
def create_admin():
    """Create the default admin user if it doesn't already exist."""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
        ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'password')
        ADMIN_EMAIL    = os.environ.get('ADMIN_EMAIL', 'admin@example.com')

        if not User.objects.filter(username=ADMIN_USERNAME).exists():
            User.objects.create_superuser(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD,
                role='admin',        # custom field on core.User
            )
            print(f"[WSGI] Admin user '{ADMIN_USERNAME}' created successfully.")
        else:
            print(f"[WSGI] Admin user '{ADMIN_USERNAME}' already exists — skipped.")
    except Exception as exc:
        # Never crash the server because of this; just log the error.
        print(f"[WSGI] Could not create admin user: {exc}")


create_admin()
