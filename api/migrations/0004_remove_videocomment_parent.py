# Generated by Django 4.2.1 on 2024-06-17 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_videocomment_parent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='videocomment',
            name='parent',
        ),
    ]
