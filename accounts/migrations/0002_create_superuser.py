from django.db import migrations
import os


def create_superuser(apps, schema_editor):
    from django.contrib.auth.models import User
    from accounts.models import Profile

    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if not username or not password:
        return

    User.objects.filter(username=username).delete()

    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )

    Profile.objects.get_or_create(user=user)


def delete_superuser(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser, delete_superuser),
    ]