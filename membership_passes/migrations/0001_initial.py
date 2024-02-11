# Generated by Django 5.0 on 2024-02-11 18:03

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sections', '0005_remove_sectionmodel_students'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PassModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('qr_code', models.CharField(max_length=255, unique=True,
                                             validators=[django.core.validators.URLValidator])),
                ('quantity_lessons_max', models.PositiveIntegerField(default=0)),
                ('is_unlimited', models.BooleanField()),
                ('is_active', models.BooleanField(default=True)),
                ('valid_from', models.DateField()),
                ('valid_until', models.DateField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('is_paid', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='section_passes', to='sections.sectionmodel')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='my_passes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EntryModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('to_pass', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                              related_name='entries', to='membership_passes.passmodel')),
            ],
        ),
    ]
