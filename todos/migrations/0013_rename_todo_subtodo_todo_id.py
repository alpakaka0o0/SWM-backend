# Generated by Django 5.0.6 on 2024-10-08 07:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0012_rename_end_date_todo_date_remove_todo_start_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subtodo',
            old_name='todo',
            new_name='todo_id',
        ),
    ]