# Generated by Django 3.0.6 on 2020-05-29 17:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qnA', '0006_auto_20200527_2352'),
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mycomment',
            name='title',
        ),
        migrations.AddField(
            model_name='mycomment',
            name='ans',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='qnA.Answer'),
            preserve_default=False,
        ),
    ]
