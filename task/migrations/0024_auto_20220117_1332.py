# Generated by Django 3.2.8 on 2022-01-17 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0023_alter_task_category_2'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-date_created']},
        ),
        migrations.AddField(
            model_name='withdrawal',
            name='verified',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]