# Generated by Django 2.1.7 on 2019-02-28 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Crop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ExtensionWorker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('profile_image', models.ImageField(upload_to='worker_images')),
                ('phone_number', models.IntegerField()),
                ('started_work', models.DateField()),
                ('gender', models.CharField(max_length=8)),
            ],
        ),
        migrations.CreateModel(
            name='Farm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farmer_name', models.CharField(max_length=50)),
                ('village_name', models.CharField(max_length=50)),
                ('date_added', models.DateField(auto_now=True)),
                ('latitude', models.CharField(max_length=200)),
                ('longitude', models.CharField(max_length=200)),
                ('farm_code', models.CharField(max_length=200)),
                ('manager', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='processor.ExtensionWorker')),
            ],
        ),
        migrations.CreateModel(
            name='Processor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=50, null=True)),
                ('unit_of_measure', models.CharField(max_length=10, null=True)),
                ('company_image', models.ImageField(null=True, upload_to='processor_profiles')),
                ('primary_product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='processor.Crop')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('planting_date', models.DateField()),
                ('expected_harvest_date', models.DateField()),
                ('estimated_yield', models.IntegerField()),
                ('farm', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processor.Farm')),
            ],
        ),
        migrations.AddField(
            model_name='farm',
            name='processor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processor.Processor'),
        ),
        migrations.AddField(
            model_name='extensionworker',
            name='processor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='processor.Processor'),
        ),
    ]
