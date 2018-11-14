# Generated by Django 2.1.3 on 2018-11-14 09:19

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(max_length=12, unique=True, verbose_name='Unique ID')),
                ('fname', models.CharField(max_length=255, verbose_name='First Name')),
                ('lname', models.CharField(max_length=255, verbose_name='Last Name')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(blank=True, help_text="Employee's primary mobile number e.g. +91{10 digit mobile number}", max_length=128, verbose_name='Mobile Number')),
                ('email', models.EmailField(db_index=True, max_length=255, unique=True, verbose_name='email address')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('regular', 'Regular')], default='regular', max_length=15, verbose_name='Role')),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
            },
        ),
    ]