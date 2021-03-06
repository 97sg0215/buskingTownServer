# Generated by Django 2.0.4 on 2018-08-06 10:11

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
            name='Busker',
            fields=[
                ('busker_id', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('busker_name', models.CharField(blank=True, max_length=50, null=True)),
                ('team_name', models.CharField(blank=True, max_length=50, null=True)),
                ('busker_tag', models.CharField(blank=True, max_length=200, null=True)),
                ('busker_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('busker_image', models.ImageField(blank=True, null=True, upload_to='busker_profile_image/')),
                ('certification', models.NullBooleanField(default=None)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_birth', models.DateField(blank=True, null=True)),
                ('user_phone', models.CharField(blank=True, max_length=20)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
