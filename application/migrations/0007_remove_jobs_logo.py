# Generated by Django 4.0.5 on 2022-06-22 07:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0006_alter_user_data_applications'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobs',
            name='logo',
        ),
    ]
