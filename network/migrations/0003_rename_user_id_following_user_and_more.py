# Generated by Django 4.1.2 on 2022-12-29 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_user_followers_post_like_following'),
    ]

    operations = [
        migrations.RenameField(
            model_name='following',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='post_id',
            new_name='post',
        ),
        migrations.RenameField(
            model_name='like',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='user_id',
            new_name='user',
        ),
    ]
