# Generated by Django 3.2 on 2024-02-19 11:26

from django.db import migrations, models
import reviews.validators


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20240218_1452'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.SmallIntegerField(validators=[reviews.validators.validate_year], verbose_name='Год выпуска'),
        ),
    ]