# Generated by Django 5.0.2 on 2024-02-26 14:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='groupmodel',
            name='type',
        ),
        migrations.AddField(
            model_name='lessonmodel',
            name='type',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
