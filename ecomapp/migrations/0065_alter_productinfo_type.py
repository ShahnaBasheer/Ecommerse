# Generated by Django 4.1.3 on 2022-12-12 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecomapp', '0064_alter_productinfo_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productinfo',
            name='Type',
            field=models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to='ecomapp.category'),
        ),
    ]