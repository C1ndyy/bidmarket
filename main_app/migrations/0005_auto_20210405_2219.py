# Generated by Django 3.1.7 on 2021-04-05 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_auto_20210404_1625'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('Home', 'Home'), ('Fashion', 'Fashion'), ('Tech', 'Tech'), ('Sporting', 'Sporting'), ('Books', 'Books')], max_length=50),
        ),
    ]