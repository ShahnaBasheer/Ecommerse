# Generated by Django 4.1.3 on 2023-01-14 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ecommapp', '0014_remove_productinfo_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productinfo',
            name='Color',
        ),
    ]
