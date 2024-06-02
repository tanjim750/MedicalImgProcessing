# Generated by Django 3.2.16 on 2024-06-01 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app', '0005_delete_processedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProcessedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.FileField(upload_to='images')),
                ('output', models.FileField(null=True, upload_to='images')),
            ],
        ),
    ]
