# Generated by Django 3.1.3 on 2022-09-05 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zipchoAdmin', '0006_auto_20220813_0808'),
    ]

    operations = [
        migrations.CreateModel(
            name='identityDocuments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.CharField(max_length=250)),
                ('isActive', models.BooleanField(default=True)),
            ],
        ),
    ]
