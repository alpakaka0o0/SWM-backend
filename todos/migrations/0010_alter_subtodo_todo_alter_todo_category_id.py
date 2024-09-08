# Generated by Django 5.0.6 on 2024-08-23 09:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0009_alter_subtodo_todo_alter_todo_category_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtodo',
            name='todo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subtodos', to='todos.todo'),
        ),
        migrations.AlterField(
            model_name='todo',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todos.category'),
        ),
    ]
