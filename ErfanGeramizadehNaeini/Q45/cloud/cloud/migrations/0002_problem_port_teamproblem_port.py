# Generated by Django 4.2.13 on 2025-05-01 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloud', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='port',
            field=models.IntegerField(default=2000),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='teamproblem',
            name='port',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
