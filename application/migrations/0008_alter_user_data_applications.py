# Generated by Django 4.0.5 on 2022-06-22 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0007_remove_jobs_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_data',
            name='applications',
            field=models.ManyToManyField(blank=True, to='application.jobs'),
        ),
    ]