# Generated by Django 2.0.6 on 2018-07-10 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nutricionista', '0002_auto_20180614_0458'),
    ]

    operations = [
        migrations.AddField(
            model_name='nutricionista',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='nutricionista/'),
        ),
    ]
