# Generated by Django 2.0.5 on 2018-06-12 04:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0007_calculadorapiramidal_peso_a_utilizar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calculadorapiramidal',
            name='paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='calculadora', to='paciente.Paciente'),
        ),
    ]