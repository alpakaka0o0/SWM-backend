# Generated by Django 5.0.6 on 2024-07-21 04:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subtodo',
            name='order',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
