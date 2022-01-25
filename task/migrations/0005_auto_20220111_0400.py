# Generated by Django 3.2.8 on 2022-01-11 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0004_auto_20220108_2026'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_expiry_date',
            field=models.DateField(default='Jan-11-2022', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_expiry_time',
            field=models.TimeField(default='03-00-23', null=True),
        ),
    ]