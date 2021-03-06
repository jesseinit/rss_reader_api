# Generated by Django 3.2.3 on 2022-02-11 14:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feedservice', '0003_alter_feeditems_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feed',
            name='followers',
            field=models.ManyToManyField(related_name='my_feeds', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='feed',
            name='registered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
