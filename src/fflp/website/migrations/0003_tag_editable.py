# Generated by Django 3.2.9 on 2022-02-11 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_page'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='editable',
            field=models.BooleanField(default=True),
        ),
    ]
