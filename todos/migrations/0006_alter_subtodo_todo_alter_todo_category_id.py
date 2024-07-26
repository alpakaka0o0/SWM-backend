# Generated by Django 5.0.6 on 2024-07-22 07:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0005_remove_subtodo_todo_id_subtodo_todo'),
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