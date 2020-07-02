# Generated by Django 3.0.6 on 2020-06-28 21:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qnA', '0012_followquestion'),
        ('notifications', '0004_auto_20200628_0011'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notif_question', to='qnA.Question'),
        ),
    ]
