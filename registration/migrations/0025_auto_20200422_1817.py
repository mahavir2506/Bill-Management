# Generated by Django 3.0.2 on 2020-04-22 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0024_auto_20200422_1817'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='sname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.Store'),
        ),
        migrations.AlterField(
            model_name='item',
            name='sname',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='registration.Store'),
        ),
    ]
