# Generated by Django 4.1.2 on 2023-01-04 11:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_rename_user_following_following_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='following',
            name='follower',
        ),
        migrations.RemoveField(
            model_name='following',
            name='following',
        ),
    ]
