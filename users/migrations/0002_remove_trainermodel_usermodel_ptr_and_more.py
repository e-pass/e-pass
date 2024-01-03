# Generated by Django 5.0 on 2024-01-03 12:59

import phonenumber_field.modelfields
from django.db import migrations, models

import users.managers


class Migration(migrations.Migration):

    dependencies = [
        ('sections', '0003_alter_groupmodel_students_alter_groupmodel_trainers_and_more'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trainermodel',
            name='usermodel_ptr',
        ),
        migrations.AlterModelManagers(
            name='usermodel',
            managers=[
                ('objects', users.managers.UserModelManager()),
                ('trainers', users.managers.TrainerManager()),
                ('students', users.managers.StudentManager()),
            ],
        ),
        migrations.AddField(
            model_name='usermodel',
            name='is_trainer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='student_parent_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='student_parent_phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, max_length=128, null=True, region='RU'),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='last_login',
            field=models.DateTimeField(editable=False, null=True),
        ),
        migrations.DeleteModel(
            name='StudentModel',
        ),
        migrations.DeleteModel(
            name='TrainerModel',
        ),
    ]
