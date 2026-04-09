from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_create_superuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='payment_confirmed',
        ),
    ]