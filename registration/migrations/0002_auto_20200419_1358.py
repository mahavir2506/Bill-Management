# Generated by Django 3.0.2 on 2020-04-19 08:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='store',
            old_name='name',
            new_name='user_name',
        ),
    ]