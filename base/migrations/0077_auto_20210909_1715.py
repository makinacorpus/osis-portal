# Generated by Django 2.2.13 on 2021-09-09 15:15

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0076_auto_20210909_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='global_id',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]
