# Generated by Django 3.1.3 on 2022-08-23 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0018_interactions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='isOnBoardingCompleted',
            field=models.BooleanField(default=False),
        ),
    ]