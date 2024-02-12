# Generated by Django 5.0 on 2024-02-12 09:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_userprofile_remove_currentevent_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='user_permissions',
        ),
        migrations.RemoveField(
            model_name='event',
            name='author',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='author',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
