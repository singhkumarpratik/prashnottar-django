# Generated by Django 3.0.6 on 2020-06-13 18:07

import autoslug.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20200613_2329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from='first_name', unique=True),
        ),
    ]
