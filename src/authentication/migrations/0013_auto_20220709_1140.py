# Generated by Django 3.1.3 on 2022-07-09 11:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0012_usertalent'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usertalent',
            old_name='talent',
            new_name='talent_id',
        ),
    ]