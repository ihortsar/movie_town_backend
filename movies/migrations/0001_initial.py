# Generated by Django 5.0.2 on 2024-04-10 10:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(default=datetime.date.today)),
                ('title', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=150)),
                ('video_file', models.FileField(blank=True, null=True, upload_to='videos')),
            ],
        ),
    ]
