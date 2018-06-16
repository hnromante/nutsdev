# Generated by Django 2.0.5 on 2018-06-14 04:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('paciente', '0009_auto_20180612_1922'),
    ]

    operations = [
        migrations.CreateModel(
            name='AntecedentesAlimentarios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('perdida_peso', models.FloatField(blank=True, default=0, null=True)),
                ('ganancia_peso', models.FloatField(blank=True, default=0, null=True)),
                ('dif_deglucion', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('apetito', models.CharField(choices=[('BA', 'Baja'), ('ME', 'Media'), ('AL', 'Alta')], default='BA', max_length=2)),
                ('vomito', models.BooleanField(default=False)),
                ('nauseas', models.BooleanField(default=False)),
                ('diuresis', models.BooleanField(default=False)),
                ('intolerancia_alimentaria', models.BooleanField(default=False)),
                ('dietas', models.CharField(blank=True, default='', max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FichaBioquimica',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('colesterol_mgdl', models.FloatField(blank=True, default=0, null=True)),
                ('ldl_mgdl', models.FloatField(blank=True, default=0, null=True)),
                ('tg', models.FloatField(blank=True, default=0, null=True)),
                ('hdl', models.FloatField(blank=True, default=0, null=True)),
                ('hemoglobina_gdll', models.FloatField(blank=True, default=0, null=True)),
                ('hematocrito_gdll', models.FloatField(blank=True, default=0, null=True)),
                ('leucocitos', models.FloatField(blank=True, default=0, null=True)),
                ('plaquetas', models.FloatField(blank=True, default=0, null=True)),
                ('v_c_m', models.FloatField(blank=True, default=0, null=True)),
                ('h_c_m', models.FloatField(blank=True, default=0, null=True)),
                ('c_h_c_m', models.FloatField(blank=True, default=0, null=True)),
                ('glicemia_mgdl', models.FloatField(blank=True, default=0, null=True)),
                ('g_o_t', models.FloatField(blank=True, default=0, null=True)),
                ('g_p_t', models.FloatField(blank=True, default=0, null=True)),
                ('f_alc', models.FloatField(blank=True, default=0, null=True)),
                ('g_g_t', models.FloatField(blank=True, default=0, null=True)),
                ('bt', models.FloatField(blank=True, default=0, null=True)),
                ('bd', models.FloatField(blank=True, default=0, null=True)),
                ('e_l_p', models.FloatField(blank=True, default=0, null=True)),
                ('sodio', models.FloatField(blank=True, default=0, null=True)),
                ('potasio', models.FloatField(blank=True, default=0, null=True)),
                ('cloro', models.FloatField(blank=True, default=0, null=True)),
                ('creatinina', models.FloatField(blank=True, default=0, null=True)),
                ('v_f_g', models.FloatField(blank=True, default=0, null=True)),
                ('r_a_c', models.FloatField(blank=True, default=0, null=True)),
                ('tsh', models.FloatField(blank=True, default=0, null=True)),
                ('t3', models.FloatField(blank=True, default=0, null=True)),
                ('t4', models.FloatField(blank=True, default=0, null=True)),
                ('t_t_g_o', models.FloatField(blank=True, default=0, null=True)),
                ('glicemia_60', models.FloatField(blank=True, default=0, null=True)),
                ('glicemia_120', models.FloatField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FichaGeneral',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ocupacion', models.CharField(blank=True, default='', max_length=20)),
                ('nacionalidad', models.CharField(blank=True, default='', max_length=20)),
                ('observacion', models.TextField(blank=True, default='', max_length=500)),
                ('ultima_atencion', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FichaNutricional',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('peso', models.FloatField(blank=True, default=0, null=True)),
                ('talla', models.FloatField(blank=True, default=0, null=True)),
                ('imc', models.FloatField(blank=True, default=0, null=True)),
                ('diagnostico_peso', models.CharField(blank=True, default='', max_length=20, null=True)),
                ('cintura', models.FloatField(blank=True, default=0, null=True)),
                ('presion_arterial', models.FloatField(blank=True, default=0, null=True)),
                ('h_g_t', models.FloatField(blank=True, default=0, null=True)),
                ('p_bicipital', models.FloatField(blank=True, default=0, null=True)),
                ('p_tripicital', models.FloatField(blank=True, default=0, null=True)),
                ('p_sub_escapular', models.FloatField(blank=True, default=0, null=True)),
                ('p_sub_iliaco', models.FloatField(blank=True, default=0, null=True)),
                ('c_braquial', models.FloatField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='apetito',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='bd',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='bt',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='c_braquial',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='c_h_c_m',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='cintura',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='cloro',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='colesterol_mgdl',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='creatinina',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='diagnostico_peso',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='dietas',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='dif_deglucion',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='diuresis',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='e_l_p',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='f_alc',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='g_g_t',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='g_o_t',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='g_p_t',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='ganancia_peso',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='glicemia_120',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='glicemia_60',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='glicemia_mgdl',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='h_c_m',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='h_g_t',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='hdl',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='hematocrito_gdll',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='hemoglobina_gdll',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='imc',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='intolerancia_alimentaria',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='ldl_mgdl',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='leucocitos',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nacionalidad',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='nauseas',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='observacion',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='ocupacion',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='p_bicipital',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='p_sub_escapular',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='p_sub_iliaco',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='p_tripicital',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='perdida_peso',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='peso',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='plaquetas',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='potasio',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='presion_arterial',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='r_a_c',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='sodio',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='t3',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='t4',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='t_t_g_o',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='talla',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='tg',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='tsh',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='ultima_atencion',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='v_c_m',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='v_f_g',
        ),
        migrations.RemoveField(
            model_name='paciente',
            name='vomito',
        ),
        migrations.AddField(
            model_name='fichanutricional',
            name='paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paciente.Paciente'),
        ),
        migrations.AddField(
            model_name='fichageneral',
            name='paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paciente.Paciente'),
        ),
        migrations.AddField(
            model_name='fichabioquimica',
            name='paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paciente.Paciente'),
        ),
        migrations.AddField(
            model_name='antecedentesalimentarios',
            name='paciente',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paciente.Paciente'),
        ),
    ]
