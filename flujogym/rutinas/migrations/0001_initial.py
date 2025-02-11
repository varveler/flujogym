# Generated by Django 5.1.6 on 2025-02-11 01:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ejercicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre del ejercicio')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('grupo_muscular', models.CharField(choices=[('piernas', 'Piernas'), ('pecho', 'Pecho'), ('espalda', 'Espalda'), ('hombros', 'Hombros'), ('brazos', 'Brazos'), ('abdominales', 'Abdominales'), ('fullbody', 'Full Body')], max_length=50, verbose_name='Grupo muscular')),
                ('equipamiento_necesario', models.CharField(blank=True, max_length=200, verbose_name='Equipamiento necesario')),
            ],
        ),
        migrations.CreateModel(
            name='Rutina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, verbose_name='Nombre de la rutina')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('nivel_dificultad', models.CharField(choices=[('principiante', 'Principiante'), ('intermedio', 'Intermedio'), ('avanzado', 'Avanzado')], max_length=20, verbose_name='Nivel de dificultad')),
                ('duracion_estimada', models.PositiveIntegerField(verbose_name='Duración estimada (minutos)')),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
            ],
        ),
        migrations.CreateModel(
            name='EjercicioEnRutina',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orden', models.PositiveIntegerField(verbose_name='Orden')),
                ('series', models.PositiveIntegerField(verbose_name='Número de series')),
                ('repeticiones', models.CharField(max_length=50, verbose_name='Repeticiones')),
                ('descanso', models.PositiveIntegerField(verbose_name='Descanso (segundos)')),
                ('ejercicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rutinas.ejercicio')),
            ],
            options={
                'ordering': ['orden'],
            },
        ),
    ]
