# Generated by Django 5.1.2 on 2024-10-25 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0004_alter_buildingstatus_options'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BuildingStatus',
        ),
        migrations.AddField(
            model_name='profile',
            name='building1_purchased',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='building2_purchased',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='building3_purchased',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='building4_purchased',
            field=models.BooleanField(default=False),
        ),
    ]
