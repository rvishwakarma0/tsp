# Generated by Django 3.2.5 on 2021-07-19 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('TiffinServicePool', '0011_auto_20210719_1626'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratingbycoustomeronvendor',
            name='tiffin',
        ),
        migrations.AddField(
            model_name='ratingbycoustomeronvendor',
            name='vendor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='TiffinServicePool.vendor'),
        ),
    ]
