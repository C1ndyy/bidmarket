# Generated by Django 3.1.7 on 2021-04-07 18:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_auto_20210407_1420'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.listing')),
            ],
        ),
    ]
