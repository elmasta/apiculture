# Generated by Django 4.0.5 on 2022-07-13 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_alter_reply_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='approved',
            field=models.BooleanField(default=True),
        ),
    ]
