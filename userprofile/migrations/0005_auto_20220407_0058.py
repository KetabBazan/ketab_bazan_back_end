# Generated by Django 3.2 on 2022-04-06 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_alter_profile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='born_date',
            field=models.DateField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='gender',
            field=models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default=None, max_length=1, null=True),
        ),
    ]
