# Generated by Django 3.2.8 on 2022-01-14 12:45

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0017_auto_20220114_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='complaints',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 14, 12, 45, 14, 388877, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='contact',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 14, 12, 45, 14, 388877, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='earnings',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 14, 12, 45, 14, 388877, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='suscribers',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 14, 12, 45, 14, 388877, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_expiry_date',
            field=models.DateField(default=datetime.datetime(2022, 1, 14, 12, 45, 14, 388877, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='task_expiry_time',
            field=models.TimeField(default=datetime.datetime(2022, 1, 14, 12, 45, 14, 388877, tzinfo=utc), null=True),
        ),
        migrations.AlterField(
            model_name='withdrawal',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 14, 12, 45, 14, 388877, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='worker',
            name='date_created',
            field=models.DateTimeField(default=datetime.datetime(2022, 1, 14, 12, 45, 14, 388877, tzinfo=utc)),
        ),
    ]