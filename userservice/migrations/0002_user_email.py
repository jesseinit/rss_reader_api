# Generated by Django 3.2.3 on 2022-02-12 17:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userservice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(default=None, max_length=100, null=True, unique=True),
        ),
    ]
