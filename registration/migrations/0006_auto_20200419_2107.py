# Generated by Django 3.0.2 on 2020-04-19 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_store_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='store',
            name='status',
            field=models.CharField(max_length=10),
        ),
    ]