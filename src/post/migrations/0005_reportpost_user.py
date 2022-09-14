# Generated by Django 3.1.3 on 2022-08-16 08:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('post', '0004_reportpost'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportpost',
            name='user',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to='authentication.user'),
            preserve_default=False,
        ),
    ]