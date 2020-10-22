# Generated by Django 3.1.2 on 2020-10-22 07:01

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
            name='Stations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('about', models.CharField(blank=True, help_text='Short description of the station', max_length=200, null=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to=None)),
                ('register', models.CharField(help_text='Unique Register given for the Mexican Govenment', max_length=64, unique=True)),
                ('latitude', models.FloatField(max_length=9)),
                ('longitude', models.FloatField(max_length=9)),
                ('state', models.CharField(help_text='Official name of the Mexican state where is located the station', max_length=50)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(default='ghost', help_text="Station' status based on their activity. It changes when a user verify the station ", max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Prices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gas_type', models.CharField(choices=[('PR', 'Premium'), ('MG', 'Magna'), ('DS', 'Diesel')], help_text='Type of gasoline between the GAS_CHOICES', max_length=20)),
                ('price', models.FloatField(max_length=5)),
                ('date', models.DateTimeField(auto_now=True, help_text='Date Time on wich the prices are registred', verbose_name='created at')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='gasoline.stations')),
            ],
        ),
        migrations.CreateModel(
            name='Complaints',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=500)),
                ('link_evidence', models.CharField(max_length=255)),
                ('type_complaint', models.CharField(max_length=255)),
                ('date', models.DateTimeField(auto_now_add=True, help_text='Datetime when the complaint is created')),
                ('offered_price', models.FloatField(help_text='Price published in the station', max_length=5)),
                ('actual_price', models.ForeignKey(help_text='Price registered in the system when creating the complaint', on_delete=django.db.models.deletion.PROTECT, to='gasoline.prices')),
                ('station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gasoline.stations')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
