# Generated by Django 3.0.6 on 2020-06-18 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qnA', '0010_answer_pin_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='description',
        ),
    ]
