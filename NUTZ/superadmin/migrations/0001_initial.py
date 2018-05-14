# Generated by Django 2.0.5 on 2018-05-14 02:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('cho', models.IntegerField()),
                ('pro', models.IntegerField()),
                ('lip', models.IntegerField()),
                ('azu', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='GrupoAlimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('cho_prom', models.IntegerField()),
                ('pro_prom', models.IntegerField()),
                ('lip_prom', models.IntegerField()),
                ('azu_prom', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SuperAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='alimento',
            name='grupo_alimento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='superadmin.GrupoAlimento'),
        ),
    ]
