# Generated by Django 4.0.5 on 2022-07-10 00:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0003_alter_member_is_banned_alter_member_is_moderator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.member'),
        ),
    ]