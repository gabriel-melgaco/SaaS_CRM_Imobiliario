# Generated by Django 5.1.5 on 2025-02-02 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='on_trial',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='client',
            name='paid_until',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
