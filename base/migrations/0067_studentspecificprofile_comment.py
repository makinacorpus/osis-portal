# Generated by Django 2.2.13 on 2021-03-03 10:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('base', '0066_auto_20210209_1200'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentspecificprofile',
            name='arrangement_comment',
            field=models.CharField(blank=True, max_length=2000, null=True, verbose_name='Comment'),
        ),
    ]
