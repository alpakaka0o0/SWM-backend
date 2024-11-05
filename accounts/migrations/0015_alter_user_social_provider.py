# Generated by Django 4.2.16 on 2024-10-17 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_user_is_premium'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='social_provider',
            field=models.CharField(choices=[('GOOGLE', 'Google'), ('APPLE', 'Apple')], default='GOOGLE', max_length=30),
        ),
    ]