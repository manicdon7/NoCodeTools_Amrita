# Generated by Django 3.0.2 on 2023-04-16 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builder', '0007_auto_20230416_0326'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='ipfs',
            field=models.CharField(default='IPFD_ID', max_length=100),
            preserve_default=False,
        ),
    ]
