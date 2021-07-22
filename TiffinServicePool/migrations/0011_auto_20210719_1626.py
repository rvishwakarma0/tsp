# Generated by Django 3.2.5 on 2021-07-19 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('TiffinServicePool', '0010_auto_20210719_1526'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tiffin',
            old_name='image',
            new_name='photo1',
        ),
        migrations.AddField(
            model_name='tiffin',
            name='available',
            field=models.BooleanField(default=True, null=True),
        ),
        migrations.AddField(
            model_name='tiffin',
            name='photo2',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='tiffin',
            name='photo3',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='tiffin',
            name='tiffinType',
            field=models.CharField(choices=[('BREAKFAST', 'BREAKFAST'), ('LUNCH', 'LUNCH'), ('DINNER', 'DINNER')], default='3', max_length=10),
        ),
        migrations.AddField(
            model_name='tiffin',
            name='veg',
            field=models.BooleanField(default=True, null=True),
        ),
    ]