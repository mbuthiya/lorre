# Generated by Django 2.1.7 on 2019-03-09 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('processor', '0004_auto_20190309_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='season_active',
            field=models.BooleanField(default=True),
        ),
    ]
