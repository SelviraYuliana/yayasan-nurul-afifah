# Generated by Django 4.2.7 on 2024-07-01 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0036_jabatan'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Jabatan',
        ),
        migrations.AlterModelOptions(
            name='guru',
            options={'verbose_name_plural': 'Guru'},
        ),
    ]
