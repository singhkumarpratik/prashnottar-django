# Generated by Django 3.0.6 on 2020-05-27 12:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qnA', '0004_auto_20200527_0856'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='answer',
            options={'ordering': ['-vote_score']},
        ),
    ]
