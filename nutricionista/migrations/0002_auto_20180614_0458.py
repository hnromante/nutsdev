# Generated by Django 2.0.5 on 2018-06-14 04:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('nutricionista', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='menu',
            name='alimentos',
        ),
        migrations.RemoveField(
            model_name='menu',
            name='nutricionista',
        ),
        migrations.RemoveField(
            model_name='pautaalimentaria',
            name='menus',
        ),
        migrations.RemoveField(
            model_name='pautaalimentaria',
            name='nutricionista',
        ),
        migrations.DeleteModel(
            name='Menu',
        ),
        migrations.DeleteModel(
            name='PautaAlimentaria',
        ),
    ]
