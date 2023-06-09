# Generated by Django 4.2 on 2023-05-27 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('labels', '0001_initial'),
        ('tasks', '0006_alter_task_executor'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='label',
        ),
        migrations.AddField(
            model_name='task',
            name='labels',
            field=models.ManyToManyField(blank=True, related_name='labels', through='tasks.LabelM2m', to='labels.label', verbose_name='Label'),
        ),
    ]
