# Generated by Django 2.0.5 on 2018-06-14 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('nutricionista', '0002_auto_20180614_0458'),
        ('paciente', '0011_auto_20180614_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atencion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('observacion', models.CharField(max_length=200)),
                ('fecha', models.DateField(blank=True, null=True)),
                ('hora', models.TimeField(blank=True, null=True)),
                ('nutricionista', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='nutricionista.Nutricionista')),
                ('paciente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paciente.Paciente')),
            ],
        ),
    ]