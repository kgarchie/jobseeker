# Generated by Django 4.0.5 on 2022-06-22 05:37

import datetime
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
            name='Jobs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(default='Local Business', max_length=20)),
                ('title', models.CharField(max_length=20)),
                ('category', models.CharField(default='General', max_length=10)),
                ('description', models.TextField(blank=True, null=True)),
                ('location', models.CharField(max_length=20)),
                ('vacancies', models.IntegerField()),
                ('salary', models.IntegerField()),
                ('payout', models.CharField(choices=[('One Time', 'One Time'), ('Weekly', 'Weekly'), ('Fortnight', 'Fortnight'), ('Monthly', 'Monthly')], default='Monthly', max_length=20)),
                ('qualifications', models.CharField(choices=[('PHD', 'PHD'), ('Degree', 'Degree'), ('Diploma', 'Diploma'), ('Certificate', 'Certificate'), ('High School', 'High School')], default='Degree', max_length=20)),
                ('date_posted', models.DateField(default=datetime.date(2022, 6, 22))),
            ],
            options={
                'verbose_name_plural': 'Jobs',
            },
        ),
        migrations.CreateModel(
            name='User_data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dob', models.DateField()),
                ('city', models.CharField(max_length=20)),
                ('highQ', models.CharField(choices=[('PHD', 'PHD'), ('Degree', 'Degree'), ('Diploma', 'Diploma'), ('Certificate', 'Certificate'), ('High School', 'High School')], default='Degree', max_length=20)),
                ('institution', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Non-Binary', 'Non-Binary')], default='Nairobi', max_length=20)),
                ('dog', models.DateField()),
                ('applications', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='application.jobs')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'User Data',
            },
        ),
    ]