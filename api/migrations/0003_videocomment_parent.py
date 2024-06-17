# Generated by Django 4.2.1 on 2024-06-17 14:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_videocomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='videocomment',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='api.videocomment'),
        ),
    ]
