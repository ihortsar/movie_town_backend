# Generated by Django 5.0.2 on 2024-04-23 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_customuser_selected_movies_alter_customuser_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='selected_movies',
            field=models.JSONField(blank=True, default=list),
        ),
    ]
